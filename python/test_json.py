import json

with open('sample.json') as file:
    datas = json.load(file)

# 결과 리스트에서 첫 번째 항목을 가져옵니다
results = datas.get('results', [])

if results:
    # 첫 번째 항목에서 lexicalEntries를 가져옴
    lexical_entries = results[0].get('lexicalEntries', [])

    # 추출할 데이터를 저장할 리스트
    extracted_data = []

    for lexical_entry in lexical_entries:
        # senses에서 definitions과 examples의 text 추출
        entries = lexical_entry.get('entries', [])
        if not entries:
            continue
        entry = entries[0]
        senses = entry.get('senses', [])

        for sense in senses:
            # definitions
            definitions = sense.get('definitions', [])
            # examples의 text
            examples = [example.get('text') for example in sense.get('examples', [])]

            # subsenses에서 definitions과 examples 추출
            subsenses = sense.get('subsenses', [])
            for subsense in subsenses:
                subsense_definitions = subsense.get("definitions", [])
                subsense_examples = [example.get('text') for example in subsense.get('examples', [])]

                # 추출한 데이터를 저장
                extracted_data.append({
                    'definitions': subsense_definitions,
                    'examples': subsense_examples
                })

            # 만약 subsenses가 없다면, 기존의 sense 데이터도 추가
            extracted_data.append({
                'definitions': definitions,
                'examples': examples
            })

    # 추출한 데이터 출력
    print(json.dumps(extracted_data, indent=2))
else:
    print("No data found in 'results'.")
