#!/usr/bin/python3

import re
import emoji

clean_dataset = []

def remove_names(dataset):
    pattern = re.compile(r'(.*?):\s')
    dataset = re.sub(pattern, '', dataset)
    dataset = re.sub(r'http\S+', '', dataset)
    return dataset

def random_clean(data):
    data = data.replace("this message was deleted", "")
    data = data.replace("<media omitted>", "")
    data = data.replace(":", "")

    if "added you" in data or "created group" in data or "messages and calls" in data:
        data = ""

    if len(data) > 100:
        data = ""
    return data

def convert_emoji_to_text(emoji_text):
    text_with_aliases = emoji.demojize(emoji_text)
    return text_with_aliases

with open("./dirty_data/WhatsApp Chat 2 [ES].txt", encoding="utf8") as text:
    dataset = text.read().split('\n')

for data in dataset:
    try:
        data = data.lower()
        data = remove_names(data)
        data = random_clean(data)
        data = convert_emoji_to_text(data)
        if data:
            clean_dataset.append(data)
    except:
        pass

for i, data in enumerate(clean_dataset):
    if not data:
        clean_dataset.pop(i)


print(clean_dataset)

# print(str(clean_dataset))

with open("./dirty_data/WhatsApp Chat 2 [ES]_clean.txt", "w") as f:
    for data in clean_dataset:
        f.write(str(data) + '\n')

