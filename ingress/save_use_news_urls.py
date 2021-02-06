import sys
import pickle
from w3lib.url import canonicalize_url


ct = pickle.load(open(sys.argv[1], "rb"))
for link in ct.link:
    if link is None:
        continue
    print(canonicalize_url)
