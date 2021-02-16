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
    with open(input_file, 'rb') as f:
        jlist = list(f)
        for jstr in tqdm(jlist):
            res = json.loads(jstr)
            l = str(res['language'])
            if res['maintext'] is None: continue
            if l not in textio: textio[l] = io.StringIO()
            textio[l].write(res['maintext'])
    textblob = {}
    for l in textio:
       textblob[l] = textio[l].getvalue()
       textio[l].close()
    return textblob

def bert_topic(lang, langcode, textblob):
    model = SentenceTransformer('distiluse-base-multilingual-cased-v2')
    embeddings = model.encode(textblob[langcode].split('\n')[:2000], show_progress_bar=True)
    umap_embeddings = umap.UMAP(n_neighbors=15, n_components=5, metric='cosine').fit_transform(embeddings)
    cluster = hdbscan.HDBSCAN(min_cluster_size=15, metric='euclidean', cluster_selection_method='eom').fit(umap_embeddings)
    print(cluster.labels_)

if __name__ == '__main__':
    # decompress_zstandard_to_folder('./covidstatebroadcaster.fixed.jsonl.*')
    tb = jsonl_reader('./covidstatebroadcaster.fixed.jsonl')
    bert_topic('english', 'en', tb)
