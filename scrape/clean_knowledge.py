import json

# Load raw knowledge.json
with open("knowledge.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# Recursively extract all strings
def extract_strings(obj):
    texts = []
    if isinstance(obj, str):
        texts.append(obj.strip())
    elif isinstance(obj, list):
        for item in obj:
            texts.extend(extract_strings(item))
    elif isinstance(obj, dict):
        for value in obj.values():
            texts.extend(extract_strings(value))
    return texts

# Extract and deduplicate
texts = extract_strings(raw_data)

seen = set()
cleaned_texts = []
for text in texts:
    if text and text not in seen:
        seen.add(text)
        cleaned_texts.append(text)

# Save cleaned knowledge
cleaned_data = {"data": cleaned_texts}
with open("knowledge_clean.json", "w", encoding="utf-8") as f:
    json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

print(f"✅ Cleaned {len(cleaned_texts)} unique entries saved to knowledge_clean.json")