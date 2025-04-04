import json
import pandas as pd

# sample.json 파일을 열고 데이터를 읽음
with open('sample.json') as file:
    datas = json.load(file)

results = datas.get('results', [])

if results:
    lexical_entries = results[0].get('lexicalEntries', [])

    # definitions, examples, audioFile을 각각 저장할 리스트
    definitions_data = []
    examples_data = []
    audio_files_data = []

    for lexical_entry in lexical_entries:
        entries = lexical_entry.get('entries', [])
        if entries:
            first_entry = entries[0]
            senses = first_entry.get('senses', [])

            for sense in senses:
                definitions = sense.get('definitions', [])
                examples = [example.get('text') for example in sense.get('examples', [])]

                if definitions:
                    definitions_data.append({'definitions': definitions})

                if examples:
                    examples_data.append({'examples': examples})

                subsenses = sense.get('subsenses', [])
                for subsense in subsenses:
                    sub_definitions = subsense.get("definitions", [])
                    sub_examples = [example.get('text') for example in subsense.get('examples', [])]

                    if sub_definitions:
                        definitions_data.append({'definitions': sub_definitions})

                    if sub_examples:
                        examples_data.append({'examples': sub_examples})

    # audioFile 추출
    audio_files_set = set()

    for lexical_entry in lexical_entries:
        entries = lexical_entry.get('entries', [])
        for entry in entries:
            for pron in entry.get('pronunciations', []):
                if 'audioFile' in pron:
                    audio_files_set.add(pron['audioFile'])

    # audioFiles 데이터를 리스트로 변환
    for audio in audio_files_set:
        audio_files_data.append({'audioFile': audio})

    # 각각의 데이터를 pandas DataFrame으로 변환
    definitions_df = pd.DataFrame(definitions_data)
    examples_df = pd.DataFrame(examples_data)
    audio_files_df = pd.DataFrame(audio_files_data)

    # 각 데이터를 별도의 엑셀 파일로 저장
    definitions_df.to_excel('def.xlsx', index=False, engine='openpyxl')
    examples_df.to_excel('ex.xlsx', index=False, engine='openpyxl')
    audio_files_df.to_excel('audio.xlsx', index=False, engine='openpyxl')

    print("Data has been saved to Excel files.")
else:
    print("No data found in 'results'.")
