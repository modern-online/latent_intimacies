with open("./dirty_data/translated_data.txt", encoding="utf8") as text:
    dataset = text.read().split('\n')

for i, data in enumerate(dataset):
      if not data:
            dataset.pop(i)

dialogue_pairs = [[dataset[i], dataset[i + 1]] for i in range(0, len(dataset)-1, 2)]

 
with open("./dirty_data/translated_paired.txt", "w") as f:
        f.write(str(dialogue_pairs))