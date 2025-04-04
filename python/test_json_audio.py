import json

with open('sample.json') as file:
    datas = json.load(file)

# results 리스트에서 첫 번째 항목 가져오기
results = datas.get('results', [])

if results:
    # lexicalEntries 가져오기
    lexical_entries = results[0].get('lexicalEntries', [])

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
else:
    print("No data found in 'results'.")
