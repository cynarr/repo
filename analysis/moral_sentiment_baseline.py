import json 
import numpy as np
import io
from collections import defaultdict
import sys
import os.path
from os import path
import pickle
import scipy.linalg


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

def encode(tokens, src_emb, src_word2id):   # Covariance matrix representation
    enc = np.array([src_emb[src_word2id[t]] for t in tokens if t in src_word2id])
    return np.cov(enc.T)

def multilingual_encode(tokens, src_emb, src_word2id, tgt_emb, tgt_word2id):
    """Encoder using multilingual aligned embeddings"""

    word_embs = [src_emb[src_word2id[t]] for t in tokens if t in src_word2id]
    enc = []
    for word_emb in word_embs:
        scores = (tgt_emb / np.linalg.norm(tgt_emb, 2, 1)[:, None]).dot(word_emb / np.linalg.norm(word_emb))
        enc.append(tgt_emb[scores.argmax()])

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
    vocab_count = 50000
    language_code = "de"

    # Get multilingual embeddings from https://github.com/facebookresearch/MUSE
    src_embeddings, src_id2word, src_word2id = load_vec("data/wiki.multi.en.vec", vocab_count)
    tgt_embeddings, tgt_id2word, tgt_word2id = load_vec(f"data/wiki.multi.{language_code}.vec", vocab_count)

    # Get MFT dictionary from https://osf.io/whjt2/
    mft_dict, mft_cat = load_mft_dictionary("data/mfd2.0.dic")
    moral_docs = {}

    if path.exists(".tmp/moral_doc_cache.pkl"):
        with open(".tmp/moral_doc_cache.pkl", "rb") as fp:
            moral_docs = pickle.load(fp)
    else:
        for moral_id in mft_dict:
            moral_docs[moral_id] = multilingual_encode(mft_dict[moral_id], src_embeddings, src_word2id, tgt_embeddings, tgt_word2id)
        if not path.exists(".tmp/"):
            os.mkdir(".tmp")
        with open(".tmp/moral_doc_cache.pkl", "wb") as fp:
            pickle.dump(moral_docs, fp)   

    for line in sys.stdin:
        doc = json.loads(line.strip()) 
        if doc["language"] == language_code:
            enc_doc = encode(tokenize(doc["maintext"]), src_embeddings, src_word2id)
            
            print(f'Document {doc["canon_url"]}')
            for moral_id in moral_docs:
                sentiment_score = frobenius_cosine(moral_docs[moral_id][None], enc_doc[None])[0]
                bures_sentiment_score = bures_distance(moral_docs[moral_id], enc_doc)

                print(f"{mft_cat[moral_id]} F: {sentiment_score:.3f} B: {bures_sentiment_score:.3f}", end=" ")
            print("\n")
