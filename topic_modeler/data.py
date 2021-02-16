import zstandard
import pathlib
import shutil
import json
from tqdm import tqdm
import io
# from bertopic import BERTopic

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

if __name__ == '__main__':
    # decompress_zstandard_to_folder('./covidstatebroadcaster.fixed.jsonl.*')
    tb = jsonl_reader('./covidstatebroadcaster.fixed.jsonl')
    for line in tb:
        print(line)

