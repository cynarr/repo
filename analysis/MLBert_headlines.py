MAX_LEN = 48
BATCH_SIZE = 64

import json, torch
import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification, BertConfig
from torch.utils.data import TensorDataset, DataLoader, SequentialSampler


def prepare_data(headlines):
    input_ids = []
    attention_masks = []
    for h in headlines:
        encoded_dict = tokenizer.encode_plus(h, add_special_tokens=True, max_length=MAX_LEN,
                                             pad_to_max_length=True, return_attention_mask=True, return_tensors='pt')
        input_ids.append(encoded_dict['input_ids'])
        attention_masks.append(encoded_dict['attention_mask'])

    inputs = torch.cat(input_ids, dim=0)
    masks = torch.cat(attention_masks, dim=0)

    data = TensorDataset(inputs, masks)
    sampler = SequentialSampler(data)

    dataloader = DataLoader(data, sampler=sampler, batch_size=BATCH_SIZE)

    return dataloader


def predict(model, dataloader):
    print('Predicting labels for headlines...')

    model.eval()
    predictions = []

    for batch in dataloader:
        batch = tuple(t.to(device) for t in batch)

        b_input_ids, b_input_mask, b_labels = batch

        with torch.no_grad():
            outputs = model(b_input_ids, token_type_ids=None,
                            attention_mask=b_input_mask)

        logits = outputs[0]
        logits = logits.detach().cpu().numpy()

        predictions.append(logits)

    print('Done!\n')
    return predictions


if torch.cuda.is_available():
    device = torch.device("cuda")
    print('There are %d GPU(s) available.' % torch.cuda.device_count())
    print('Using', torch.cuda.get_device_name(0), ':)')
else:
    print('No GPU available, using the CPU instead.')
    device = torch.device("cpu")

data = []
with open ("covidmarch.jsonl", 'r') as json_file:
    lines = json.loads(json_file.read())
    for l in lines:
        data.append(l["title"])


df_data = pd.DataFrame.from_records(data, columns=['headline'])
print(df_data.head())

config = BertConfig.from_pretrained('config.json')
model = BertForSequenceClassification.from_pretrained('pytorch_model.bin', config=config)
model.cuda()

tokenizer = BertTokenizer.from_pretrained(model, do_lower_case=True)

dataloader = prepare_data(data)
predictions = predict(model, dataloader)
print(predictions)
