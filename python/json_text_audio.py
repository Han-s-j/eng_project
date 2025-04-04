import json

with open('sample.json') as file:
    datas = json.load(file)

# results 리스트에서 첫 번째 항목 가져오기
results = datas.get('results', [])

if results:
    # 첫 번째 항목에서 lexicalEntries를 가져옴
    lexical_entries = results[0].get('lexicalEntries', [])

    # 추출할 데이터를 저장할 리스트
    extracted_data = []

    for lexical_entry in lexical_entries:
        # pronunciations에서 audioFile 추출
        # pronunciations = lexical_entry.get('pronunciations', [])
        # audio_files = []

        # # audioFile을 포함한 항목만 추출
        # for pron in pronunciations:
        #     if 'audioFile' in pron:
        #         audio_files.append(pron['audioFile'])

        # senses에서 definitions과 examples의 text 추출
        senses = lexical_entry.get('entries', [])[0].get('senses', [])
        for sense in senses:
            # definitions
            definitions = sense.get('definitions', [])
            # examples의 text
            examples = [example.get('text') for example in sense.get('examples', [])]

            # 추출한 데이터를 저장
            extracted_data.append({
                # 'audioFiles': audio_files,
                'definitions': definitions,
                'examples': examples
            })

    # 중복을 제거할 set을 사용
    audio_files_set = set()

    for lexical_entry in lexical_entries:
        # entries 목록에서 pronunciations을 찾아 audioFile 추출
        entries = lexical_entry.get('entries', [])

        for entry in entries:
            for pron in entry.get('pronunciations', []):
                # audioFile이 존재하는지 확인
                if 'audioFile' in pron:
                    audio_files_set.add(pron['audioFile'])

    # 중복을 제외한 audioFile 리스트 출력
    for audio in audio_files_set:
        print(audio)

    # 추출한 데이터 출력
    print(json.dumps(extracted_data, indent=2))
else:
    print("No data found in 'results'.")