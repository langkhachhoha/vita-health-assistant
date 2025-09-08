import json

input_path = 'Doctor_vinmec/vinmec_doctors_database.json'
output_path = 'Doctor_vinmec/vinmec_doctors_extracted.json'

with open(input_path, 'r', encoding='utf-8') as infile:
    data = json.load(infile)

extracted = []
for item in data:
    extracted.append({
        'ten': item.get('ten_bac_si')
    })

with open(output_path, 'w', encoding='utf-8') as outfile:
    json.dump(extracted, outfile, ensure_ascii=False, indent=2)

print(extracted[58]) 