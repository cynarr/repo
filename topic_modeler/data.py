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
    links = list()
    print("Splitting articles by language:")
    with open(input_file, 'rb') as f:
        jlist = list(f)
        for jstr in tqdm(jlist):
            res = json.loads(jstr)
            l = str(res['language'])
            if res['maintext'] is None: continue
            if l not in textio: textio[l] = io.StringIO()
            textio[l].write(res['maintext'])
            links.append(res['canon_url'])
    textblob = {}
    for l in textio:
       textblob[l] = textio[l].getvalue()
       textio[l].close()
    return textblob, links

def bert_topic(lang, textblob, links):
    model = SentenceTransformer('distiluse-base-multilingual-cased-v2')
    print("Generating article embeddings for " + lang)
    embeddings = model.encode(textblob[lang].split('\n')[:20000], show_progress_bar=True)

    umap_embeddings = umap.UMAP(n_neighbors=15, n_components=5, metric='cosine').fit_transform(embeddings)
    cluster = hdbscan.HDBSCAN(min_cluster_size=15, metric='euclidean', cluster_selection_method='eom').fit(umap_embeddings)
    print(len(cluster.labels_))
    
    docs_df = pd.DataFrame(textblob[lang].split('\n')[:20000], columns=['doc'])
    docs_df['topic'] = cluster.labels_
    docs_df['doc_id'] = range(len(docs_df))
    docs_df['canon_url'] = links[:20000]
    docs_per_topic = docs_df.groupby(['topic'], as_index = False).agg({'doc': ' '.join})
    print(docs_per_topic)

if __name__ == '__main__':
    # decompress_zstandard_to_folder('./covidstatebroadcaster.fixed.jsonl.*')
    tb, links = jsonl_reader('./covidstatebroadcaster.fixed.jsonl')
    bert_topic('en', tb, links)
