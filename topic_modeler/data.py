import zstandard
import pathlib
import shutil
import json
from tqdm import tqdm
import io
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
import umap.umap_ as umap
import hdbscan
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer


TOKENIZERS_PARALLELISM = False

def decompress_zstandard_to_folder(input_file):
    input_file = pathlib.Path(input_file)
    with open(input_file, 'rb') as compressed:
        decomp = zstandard.ZstdDecompressor()
        output_path = pathlib.Path('.') / input_file.stem
        with open(output_path, 'wb') as destination:
            decomp.copy_stream(compressed, destination)
    return

def jsonl_reader(input_file):
    textio = dict() # the text for each language
    links = dict()
    print("Splitting articles by language:")
    with open(input_file, 'rb') as f:
        jlist = list(f)
        for jstr in tqdm(jlist):
            res = json.loads(jstr)
            l = str(res['language'])
            if res['maintext'] is not None and res['canon_url'] is not None: 
                if l not in textio: 
                    textio[l] = io.StringIO()
                    links[l] = list()
                textio[l].write(res['maintext'] + '\t\t')
                links[l].append(res['canon_url'])
    textblob = {}
    for l in textio:
        textblob[l] = textio[l].getvalue()
        textio[l].close()
    return textblob, links

def bert_topic(lang, textblob, links):
    model = SentenceTransformer('distiluse-base-multilingual-cased-v2')
    print("Generating article embeddings for " + lang + " en:")
    embeddings = model.encode(textblob[lang].split('\t\t'), 
            show_progress_bar=True)

    umap_embeddings = umap.UMAP(n_neighbors=15, 
            n_components=5, 
            metric='cosine').fit_transform(embeddings)
    cluster = hdbscan.HDBSCAN(min_cluster_size=15, 
            metric='euclidean', 
            cluster_selection_method='eom').fit(umap_embeddings)
    
    docs_df = pd.DataFrame(textblob[lang].split('\t\t'), 
            columns=['doc'])
    docs_df['topic'] = cluster.labels_
    docs_df['doc_id'] = range(len(docs_df))
    docs_df['canon_url'] = links[lang]
    docs_per_topic = docs_df.groupby(['topic'], 
            as_index = False).agg({'doc': ' '.join})
    return embeddings, cluster, docs_df, docs_per_topic

def c_tf_idf(docs, m, ngram_range = (1, 1)):
    count = CountVectorizer(ngram_range=ngram_range).fit(docs)
    t = count.transform(docs).toarray()
    w = t.sum(axis=1)
    tf = np.divide(t.T, w)
    sum_t = t.sum(axis=0)
    idf = np.log(np.divide(m, sum_t)).reshape(-1, 1)
    tf_idf = np.multiply(tf, idf)
    return tf_idf, count

def extract_top_n_words_per_topic(tf_idf, count, docs_per_topic, n=20):
    words = count.get_feature_names()
    labels = list(docs_per_topic.Topic)
    tf_idf_transposed = tf_idf.T
    indices = tf_idf_transposed.argsort()[:, -n:]
    top_n_words = {label: [(words[j], tf_idf_transposed[i][j]) for j in indices[i]][::-1] for i, label in enumerate(labels)}
    return top_n_words

def extract_topic_sizes(df):
    topic_sizes = (df.groupby(['Topic'])
                     .Doc
                     .count()
                     .reset_index()
                     .rename({"Topic": "Topic", "Doc": "Size"}, axis='columns')
                     .sort_values("Size", ascending=False))
    return topic_sizes

def topic_per_link(top_n_words, docs):
    pass

if __name__ == '__main__':
    # decompress_zstandard_to_folder('./covidstatebroadcaster.fixed.jsonl.*')
    tb, links = jsonl_reader('./covidstatebroadcaster.fixed.jsonl')
    em, clusters, docs_df, docs_per_topic = bert_topic('en', tb, links)
    # print(tb['en'])
    tf_idf, count = c_tf_idf(docs_per_topic.Doc.values, m=len(data))
    top_n_words = extract_top_n_words_per_topic(tf_idf, count, docs_per_topic, n=20)
    topic_sizes = extract_topic_sizes(docs_df); topic_sizes.head(10)
    print(topic_sizes)
