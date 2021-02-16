import os
import torch
import orjson
import sys
import click
from transformers import (
    BertTokenizerFast,
    BertForSequenceClassification,
    BertConfig
)
from torch.utils.data import (
    DataLoader,
    IterableDataset
)


DIR_PATH = os.path.dirname(os.path.realpath(__file__))
CONFIG_PATH = os.path.join(
    DIR_PATH,
    "news_sentiment_config.json"
)
MODEL_PATH = os.environ.get(
    "NEWS_SENTIMENT_MODEL",
    os.path.join(
        DIR_PATH,
        "..",
        "data",
        "news_sentiment_model.bin"
    )
)
LABELS = ["negative", "neutral", "positive"]


DEFAULT_BATCH_SIZE = 64


class DocumentIteratorDataset(IterableDataset):
    def __iter__(self):
        for _id, line in enumerate(sys.stdin.buffer):
            doc = orjson.loads(line)
            canon_url = doc["canon_url"]
            title = doc["title"]
            yield canon_url, title


@click.command()
@click.option("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
def main(batch_size):
    if torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")

    tokenizer = BertTokenizerFast.from_pretrained(
        "bert-base-multilingual-cased",
        do_lower_case=True
    )
    config = BertConfig.from_pretrained(CONFIG_PATH)
    model = BertForSequenceClassification.from_pretrained(
        MODEL_PATH,
        config=config
    )
    if torch.cuda.is_available():
        model.cuda()
    else:
        print("Warning: using CPU", file=sys.stderr)
    model.eval()

    dataset = DocumentIteratorDataset()
    dataloader = DataLoader(dataset, batch_size=batch_size)

    with torch.no_grad():
        for batch in dataloader:
            token_batch = tokenizer(
                list(batch[1]),
                return_tensors="pt",
                padding=True,
                truncation=True
            )
            token_batch.to(device)

            outputs = model(
                token_batch.input_ids,
                token_type_ids=token_batch.token_type_ids,
                attention_mask=token_batch.attention_mask
            )
            labels_idxs = torch.argmax(outputs[0], dim=1).detach()

            for curl, label_idx in zip(batch[0], labels_idxs):
                sys.stdout.buffer.write(orjson.dumps({
                    "canon_url": curl,
                    "sentiment": LABELS[label_idx],
                }))
                sys.stdout.buffer.write(b"\n")


if __name__  == "__main__":
    main()
