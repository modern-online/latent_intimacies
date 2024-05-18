from deep_translator import GoogleTranslator

file_name = "YOUR FILE TO BE TRANSLATED"

with open(file_name, encoding="utf8") as text:
    dataset = text.read().split("\n")

for data in dataset:
    if data:
        try:
            print(data)
            #res = ts.translate_text(data, translator='niutrans', to_language='en')
            res = GoogleTranslator(source='auto', target='en').translate(data)
            with open("./dirty_data/translated_data.txt", "a+") as f:
                f.write(res + "\n")
        except(KeyboardInterrupt):
            break
        except Exception as e:
            print(e)
            print("IGNORED")

            pass
