#!/usr/bin/python3

import re
import emoji


def remove_names(dataset):
    pattern = re.compile(r'\[.*\].*:\s')
    dataset = re.sub(pattern, '', dataset)
    return dataset

def convert_emoji_to_text(emoji_text):
    text_with_aliases = emoji.demojize(emoji_text)
    return text_with_aliases

with open("./dirty_data/data.txt", encoding="utf8") as text:
    dataset = text.read()

dataset = remove_names(dataset)
dataset = convert_emoji_to_text(dataset)
dataset = dataset.split("\n")[1:-1]
dataset = [dataset[i:i+2] for i in range(0, len(dataset), 2)]

with open("./clean_data/clean_data.txt", "w") as f:
    f.write(str(dataset))


print(dataset)
