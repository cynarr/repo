import nltk 
from nltk.corpus import wordnet 
from collections import defaultdict
import pickle

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


def get_antonym(word):
    # TODO: maybe should consider synonyms also
    for t in ["a", "v", "n"]:
        try:
            antonyms = wordnet.synset(f"{word}.{t}.01").lemmas()[0].antonyms() 
            if len(antonyms) > 0:
                return antonyms[0].name()
        except LookupError:
            print("ERROR:")
            print("Download Wordnet first running: nltk.download('wordnet')")
            exit()
        except:
            pass

    return ""

def generate_list(virtues, vices):
    word_pairs = []
    for virtue in virtues:
        antonym = get_antonym(virtue)
        if antonym in vices: # TODO: might be too strict condition
            word_pairs.append((virtue, antonym))
    return word_pairs        

if __name__ == "__main__":
    mft_dict, mft_cat = load_mft_dictionary("data/mfd2.0.dic")

    word_pairs_dict = defaultdict(list)

    for i in range(0,5):
        key = mft_cat[i*2+1].split(".")[0]
        word_pairs_dict[key] += generate_list(mft_dict[i*2+1], mft_dict[i*2+2])
        word_pairs_dict[key] += [(b ,a) for (a, b) in generate_list(mft_dict[i*2+2], mft_dict[i*2+1])]

    for key in word_pairs_dict:
        word_pairs_dict[key] = sorted(set(word_pairs_dict[key]), key=lambda x: x[0])

    with open("data/mft_sentiment_word_pairs.pkl", "wb") as fp:
        pickle.dump(word_pairs_dict, fp)
