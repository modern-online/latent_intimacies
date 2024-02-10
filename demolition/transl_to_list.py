with open("./dirty_data/translated_data.txt", encoding="utf8") as text:
    dataset = text.read().split('\n')

for i, data in enumerate(dataset):
      if not data:
            dataset.pop(i)

with open("./dirty_data/translated_list.txt", "w") as f:
        f.write(str(dataset))