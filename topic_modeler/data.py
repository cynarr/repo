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
            if res['maintext'] is not None: 
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
    print("Generating article embeddings for " + lang + ":")
    embeddings = model.encode(textblob[lang].split('\t\t')[:-1], 
            show_progress_bar=True)
    try:
        umap_embeddings = umap.UMAP(n_neighbors=15, 
                n_components=5, 
                metric='cosine').fit_transform(embeddings)
    except:
        return
    cluster = hdbscan.HDBSCAN(min_cluster_size=15, 
            metric='euclidean', 
            cluster_selection_method='eom').fit(umap_embeddings)
    
    docs_df = pd.DataFrame(textblob[lang].split('\t\t')[:-1], 
            columns=['doc'])
    docs_df['topic'] = cluster.labels_
    docs_df['doc_id'] = range(len(docs_df))
    docs_df['canon_url'] = links[lang]
    docs_per_topic = docs_df.groupby(['topic'], 
            as_index = False).agg({'doc': ' '.join})
    # print(docs_df)
    return embeddings, cluster, docs_df, docs_per_topic

def c_tf_idf(docs, m, stop_words=None, ngram_range = (1, 1)):
    try:
        count = CountVectorizer(ngram_range=ngram_range, stop_words=stop_words, min_df=0.1, max_df=0.8).fit(docs)
    except:
        return 
    t = count.transform(docs).toarray()
    w = t.sum(axis=1)
    tf = np.divide(t.T, w)
    sum_t = t.sum(axis=0)
    idf = np.log(np.divide(m, sum_t)).reshape(-1, 1)
    tf_idf = np.multiply(tf, idf)
    return tf_idf, count

def extract_top_n_words_per_topic(tf_idf, count, docs_per_topic, n=20):
    words = count.get_feature_names()
    labels = list(docs_per_topic.topic)
    tf_idf_transposed = tf_idf.T
    indices = tf_idf_transposed.argsort()[:, -n:]
    top_n_words = {label: [(words[j]) for j in indices[i]][::-1] for i, label in enumerate(labels)}
    return top_n_words

def extract_topic_sizes(df):
    topic_sizes = (df.groupby(['topic'])
                     .doc
                     .count()
                     .reset_index()
                     .rename({"topic": "topic", "doc": "size"}, axis='columns')
                     .sort_values("size", ascending=False))
    return topic_sizes

def topic_per_link(top_n_words, docs_df):
    url_topic_mapping = list()
    for ix in range(len(docs_df['canon_url'])): 
        mapping = dict()
        mapping['canon_url'] = docs_df['canon_url'][ix]
        mapping['topics'] = top_n_words[docs_df['topic'][ix]][:5]
        url_topic_mapping.append(mapping)
    return url_topic_mapping

if __name__ == '__main__':
    # decompress_zstandard_to_folder('./covidstatebroadcaster.fixed.jsonl.*')
    tb, links = jsonl_reader('./covidstatebroadcaster.fixed.jsonl')
    with open('./stopwords-all.json', 'r') as s:
        stop_words_all = json.load(s)
    url_topic_dict = dict()
    fp = open('url_topic.json', 'a+')
    for lang in tb:
        em, clusters, docs_df, docs_per_topic = bert_topic(lang, tb, links)
        if len(tb[lang].split('\t\t')[:-1]) < 10:
            continue
        try:
            tf_idf, count = c_tf_idf(docs_per_topic.doc.values, 
                    len(tb[lang]), 
                    stop_words=stop_words_all[lang])
        except TypeError:
            continue
        except:
            tf_idf, count = c_tf_idf(docs_per_topic.doc.values,
                    len(tb[lang]))
        top_n_words = extract_top_n_words_per_topic(tf_idf, count, docs_per_topic, n=20)
        topic_sizes = extract_topic_sizes(docs_df)
        url_topic_lang = topic_per_link(top_n_words, docs_df)
        print(url_topic_lang)
        json.dump(url_topic_lang, fp)
