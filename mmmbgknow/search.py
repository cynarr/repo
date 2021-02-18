import re2
import transformers
from itertools import groupby


REMOVED_TOKEN = "__REMOVED_FROM_VOCAB__"


def get_tokenizer():
    tokenizer = transformers.XLMRobertaTokenizer.from_pretrained(
        "xlm-roberta-large"
    )
    filtered_vocab = [
        tokenizer.sp_model.id_to_piece(id)
        if len(tokenizer.sp_model.id_to_piece(id)) <= 4
        else REMOVED_TOKEN
        for id in range(tokenizer.sp_model.get_piece_size())
    ]
    tokenizer.sp_model.set_vocabulary(filtered_vocab)
    return tokenizer


def word_segs(tokenizer, keyword):
    result = []
    tokenized = tokenizer.tokenize(keyword)
    head = None
    for token in tokenized:
        if token.startswith("▁"):
            head = []
            result.append(head)
            token = token[1:]
        head.append(token.encode("utf-8"))
    return result


def keyword_stem_regex(tokenizer, keyword, name=None):
    keyword_re = []
    word_tokens = word_segs(tokenizer, keyword.lower())
    for word in word_tokens:
        allow_ending = (
            all((tok.isalpha() for tok in word)) and len(word) >= 2
        )
        letters_stemmed = len("".join((w.decode("utf-8") for w in word[:-1])))
        do_stem = allow_ending and len(word) >= 3 and letters_stemmed >= 4
        if do_stem:
            del word[-1]
        joined = b"".join(word)
        keyword_re.append(
            re2.escape(joined) +
            (br"\pL*" if allow_ending else b"")
        )
    if not keyword_re:
        return None
    if name is not None:
        capture_group = b"?P<%s>" % name.encode("utf-8")
    else:
        capture_group = b""
    return (
        br"(" + capture_group +
        br"\s+".join(keyword_re) +
        br")"
    )


def join_re_bits(re_bits):
    return br"(?:\A|(?:\s+))(?:" + b"|".join(re_bits) + br")(?:\z|(?:\s+))"


class MatchSearcher:
    def __init__(self, keywords, extra_patterns=None):
        tokenizer = get_tokenizer()
        re_bits = []
        for keyword in keywords:
            pattern = keyword_stem_regex(tokenizer, keyword)
            if pattern is None:
                continue
            re_bits.append(pattern)
        if extra_patterns is not None:
            re_bits.extend(extra_patterns)
        regex = join_re_bits(re_bits)
        self.matcher = re2.compile(regex)

    def match(self, haystack):
        return self.matcher.contains(haystack)


def get_re_bits(keywords):
    tokenizer = get_tokenizer()
    re_bits = []
    for output, keywords in keywords.items():
        for idx, keyword in enumerate(keywords):
            pattern = keyword_stem_regex(
                tokenizer,
                keyword,
                name=f"{output}_{idx}"
            )
            if pattern is None:
                continue
            re_bits.append(pattern)
    return re_bits


class MapSearcher:
    def __init__(self, keywords):
        re_bits = get_re_bits(keywords)
        regex = join_re_bits(re_bits)
        self.matcher = re2.compile(regex)

    def match(self, haystack):
        position = 0
        result = set()
        while 1:
            match = self.matcher.search(haystack, position)
            if not match:
                break
            group = match.lastgroup
            position = match.end(group)
            item = group.rsplit("_", 1)[0]
            result.add(item)
        return result
