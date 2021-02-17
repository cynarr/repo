import json 
import numpy as np
import io
from collections import defaultdict
import sys
import os.path
from os import path
import pickle
import scipy.linalg
import pickle
import requests


MFT_SENTIMENT_WORD_PAIRS = os.environ.get("MFT_SENTIMENT_WORD_PAIRS", "data/mft_sentiment_word_pairs.pkl")
MFD20 = os.environ.get("MFD20", "data/mfd2.0.dic")
MUSE = os.environ.get("MUSE", "data/muse")


def load_vec(emb_path, nmax=50000):
    vectors = []
    word2id = {}
    with io.open(emb_path, 'r', encoding='utf-8', newline='\n', errors='ignore') as f:
        next(f)
        for _, line in enumerate(f):
            word, vect = line.rstrip().split(' ', 1)
            vect = np.fromstring(vect, sep=' ')
            assert word not in word2id, 'word found twice'
            vectors.append(vect)
            word2id[word] = len(word2id)
            if len(word2id) == nmax:
                break
    id2word = {v: k for k, v in word2id.items()}
    embeddings = np.vstack(vectors)
    return embeddings, id2word, word2id

def compute_moral_dimensions(word_pair_dict, src_emb, src_word2id, tgt_emb, tgt_word2id):
    # Following the idea introduced here: https://journals.sagepub.com/doi/full/10.1177/0003122419877135

    moral_vectors = {}
    for sent in word_pair_dict:
        vecs = []
        for a,b in word_pair_dict[sent]:
            if a in src_word2id and b in src_word2id:
                w1 = src_emb[src_word2id[a]]
                w2 = src_emb[src_word2id[b]]

                pos = get_approx_translated_word(w1, src_emb, src_word2id, tgt_emb, tgt_word2id)
                neg = get_approx_translated_word(w2, src_emb, src_word2id, tgt_emb, tgt_word2id)

                vecs.append(pos - neg)
        moral_vectors[sent] = np.array(vecs).sum(0)
        moral_vectors[sent] = moral_vectors[sent] / np.linalg.norm(moral_vectors[sent]) # Normalize to unit length so that all moral dimensions are equal
    return moral_vectors

def project_document_to_moral_dim(doc, moral_vector): # Assumes moral vector are normalized to unit length
    return (moral_vector[None] @ doc.T).sum() # TODO: Possibly should be mean, so that the document length does not affect the score

def load_mft_dictionary(path):
    with open(path, "r") as fp:
        data = fp.readlines()
    
    categories = {}
    items = defaultdict(list)
    for row in data[1:11]:
        cat_id, description = row.strip().split("\t")
        categories[int(cat_id)] = description

    for row in data[12:]:    
        word, cat_id = row.strip().split("\t")
        items[int(cat_id)].append(word)

    return items, categories

def tokenize(text):
    tokens = text.split()
    return tokens

def create_doc_matrix(tokens, src_emb, src_word2id):
    return np.array([src_emb[src_word2id[t]] for t in tokens if t in src_word2id])

def encode(doc_matrix, src_emb, src_word2id):   # Covariance matrix representation
    return np.cov(doc_matrix.T)

def get_approx_translated_word(word_emb, src_emb, src_word2id, tgt_emb, tgt_word2id):
    scores = (tgt_emb / np.linalg.norm(tgt_emb, 2, 1)[:, None]).dot(word_emb / np.linalg.norm(word_emb))
    return tgt_emb[scores.argmax()]

def multilingual_encode(tokens, src_emb, src_word2id, tgt_emb, tgt_word2id):
    """Encoder using multilingual aligned embeddings"""

    word_embs = [src_emb[src_word2id[t]] for t in tokens if t in src_word2id]
    enc = []
    for word_emb in word_embs:
        enc.append(get_approx_translated_word(word_emb, src_emb, src_word2id, tgt_emb, tgt_word2id))

    enc = np.array(enc)
    return np.cov(enc.T)

def frobenius_cosine(A, B):
    """Computes normalized Frobenius inner product"""

    return np.sum(A * B, axis=(1, 2)) / (np.sqrt(np.sum(A * A, axis=(1, 2))) * np.sqrt(np.sum(B * B, axis=(1, 2))))

def bures_distance(A, B):
    """Computes Bures-Wasserstein distance that should match to word movers distance
    
    Implemented following https://arxiv.org/pdf/1712.01504.pdf. Seems to be numerically instabile
    """
    
    A_sqrt = scipy.linalg.sqrtm(A)
    AB_sqrt = scipy.linalg.sqrtm(A_sqrt @ B @ A_sqrt)
    distance = np.sqrt(np.trace(A) + np.trace(B) - 2 * np.trace(AB_sqrt))

    return np.real(distance)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error: Input language code to use e.g. 'de'", file=sys.stderr)
        exit()

    vocab_count = 100000
    language_code = sys.argv[1]

    # Get multilingual embeddings from https://github.com/facebookresearch/MUSE
    src_embeddings, src_id2word, src_word2id = load_vec(os.path.join(MUSE, "wiki.multi.en.vec"), vocab_count)
    tgt_embeddings, tgt_id2word, tgt_word2id = load_vec(os.path.join(MUSE, f"wiki.multi.{language_code}.vec"), vocab_count)

    # Compute moral dimensions, compute the .pkl file with with analysis/sentiment_antonym_pair_util.py
    with open(MFT_SENTIMENT_WORD_PAIRS, "rb") as fp:
        moral_word_pairs = pickle.load(fp)
        moral_dims = compute_moral_dimensions(moral_word_pairs, src_embeddings, src_word2id, tgt_embeddings, tgt_word2id)

    # Get MFT dictionary from https://osf.io/whjt2/
    mft_dict, mft_cat = load_mft_dictionary(MFD20)
    moral_docs = {}

    if path.exists(f".tmp/moral_doc_cache_{language_code}.pkl"):
        with open(f".tmp/moral_doc_cache_{language_code}.pkl", "rb") as fp:
            moral_docs = pickle.load(fp)
    else:
        for moral_id in mft_dict:
            moral_docs[moral_id] = multilingual_encode(mft_dict[moral_id], src_embeddings, src_word2id, tgt_embeddings, tgt_word2id)
        if not path.exists(".tmp/"):
            os.mkdir(".tmp")
        with open(f".tmp/moral_doc_cache_{language_code}.pkl", "wb") as fp:
            pickle.dump(moral_docs, fp)   

    for line in sys.stdin:
        doc = json.loads(line.strip())
        json_obj = {}        
        if doc["language"] == language_code:
            json_obj["canon_url"] = doc["canon_url"]
            json_obj["bures_sentiment"] = {}
            json_obj["frob_sentiment"] = {}
            json_obj["proj_sentiment"] = {}
            
            doc_matrix = create_doc_matrix(tokenize(doc["maintext"]), src_embeddings, src_word2id)
            enc_doc = encode(doc_matrix, src_embeddings, src_word2id)
            
            for moral_id in moral_docs:
                sentiment_score = frobenius_cosine(moral_docs[moral_id][None], enc_doc[None])[0]
                bures_sentiment_score = bures_distance(moral_docs[moral_id], enc_doc)
                json_obj["frob_sentiment"][mft_cat[moral_id]] = sentiment_score
                json_obj["bures_sentiment"][mft_cat[moral_id]] = bures_sentiment_score
            
            for moral_dim in moral_dims:
                json_obj["proj_sentiment"][moral_dim] = project_document_to_moral_dim(doc_matrix, moral_dims[moral_dim])
            
            print(json.dumps(json_obj))
