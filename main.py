import json
from googletrans import Translator

FILE = 'input.json'
LANGUAGES = ['ru', 'kk']

translator = Translator()

f = open(FILE, 'r', encoding='utf-8')
data = json.load(f)
f.close()

results = {}

def translate_data(data, lang, count):
    if isinstance(data, dict):
        translated_data = {}
        for key, value in data.items():
            translated_data[key] = translate_data(value, lang, count)
            count[0] += 1  # Increment the count
            print(f"Progress: {count[0]}/{count[1]}")  # Print the progress
        return translated_data
    elif isinstance(data, list):
        translated_data = []
        for item in data:
            translated_data.append(translate_data(item, lang, count))
            count[0] += 1  # Increment the count
            print(f"Progress: {count[0]}/{count[1]}")  # Print the progress
        return translated_data
    else:
        count[0] += 1  # Increment the count
        print(f"Progress: {count[0]}/{count[1]}")  # Print the progress
        return translator.translate(data, dest=lang).text

def count_keys(data):
    count = 0
    if isinstance(data, dict):
        count += len(data.keys())
        for value in data.values():
            count += count_keys(value)
    elif isinstance(data, list):
        for item in data:
            count += count_keys(item)
    else:
        count += 1
    return count

total_keys = count_keys(data)  # Get the total number of keys

for lang in LANGUAGES:
    count = [0, total_keys]  # Initialize the count
    results[lang] = translate_data(data, lang, count)

    for lang, translated_data in results.items():
        output_file = f'output/{lang}.json'
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(translated_data, f, ensure_ascii=False, indent=4)
            print(f"Translation to {lang} completed.")
        except Exception as e:
            print(f"Error writing to {output_file}: {e}")
