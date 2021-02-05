import json 
import numpy as np
import io
from collections import defaultdict


def load_vec(emb_path, nmax=50000):
    vectors = []
    word2id = {}
    with io.open(emb_path, 'r', encoding='utf-8', newline='\n', errors='ignore') as f:
        next(f)
        for i, line in enumerate(f):
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

def encode(tokens, src_emb, src_word2id):   # Covariance matric representation
    enc = np.array([src_emb[src_word2id[t]] for t in tokens if t in src_word2id])
    return np.cov(enc.T)

def multilingual_encode(tokens, src_emb, src_word2id, tgt_emb, tgt_word2id):
    """Encoder using multilingual embeddings"""

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


nmax = 50000
language_code = "de"

# Get multilingual embeddings from https://github.com/facebookresearch/MUSE

src_embeddings, src_id2word, src_word2id = load_vec("data/wiki.multi.en.vec", nmax)
tgt_embeddings, tgt_id2word, tgt_word2id = load_vec(f"data/wiki.multi.{language_code}.vec", nmax)


# Get MFT dictionary from https://osf.io/whjt2/
mft_dict, mft_cat = load_mft_dictionary("data/mfd2.0.dic")

moral_docs = {}
for moral_id in mft_dict:
    moral_docs[moral_id] = multilingual_encode(mft_dict[moral_id], src_embeddings, src_word2id, tgt_embeddings, tgt_word2id)

with open("data/covidmarch.jsonl", encoding="utf-8") as fp:
    docs = [json.loads(jline) for jline in fp.read().splitlines()]
    enc_docs = []
    for doc in docs:
        if doc["language"] == language_code:
            enc_docs.append(encode(tokenize(doc["maintext"]), src_embeddings, src_word2id))

enc_docs = np.array(enc_docs)

moral_sentiments = {}
for moral_id in moral_docs:
    print(f"Scoring {mft_cat[moral_id]}...")
    moral_sentiments[moral_id] = frobenius_cosine(moral_docs[moral_id][None], enc_docs)