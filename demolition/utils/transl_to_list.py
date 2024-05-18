input_data_path = "YOUR TRANSLATED DATA FILE.txt"
output_data_path = "YOUR OUTPUT FILE.txt"

with open(input_data_path, encoding="utf8") as text:
    dataset = text.read().split('\n')

for i, data in enumerate(dataset):
      if not data:
            dataset.pop(i)

with open(output_data_path, "w") as f:
        f.write(str(dataset))
