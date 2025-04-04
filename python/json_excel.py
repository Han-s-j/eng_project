import json
import pandas
import pandas as pd

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
        senses = lexical_entry.get('entries', [])[0].get('senses', [])
        for sense in senses:
            # definitions
            definitions = sense.get('definitions', [])
            # examples의 text
            examples = [example.get('text') for example in sense.get('examples', [])]

            # definitions과 examples가 모두 있을 때만 데이터 추가
            if definitions and examples:
                extracted_data.append({
                    'definitions': definitions,
                    'examples': examples
                })

            # subsenses 처리
            subsenses = sense.get('subsenses', [])
            for subsense in subsenses:
                sub_definitions = subsense.get("definitions", [])
                sub_examples = [example.get('text') for example in subsense.get('examples', [])]

                # subsense의 definitions과 examples가 모두 있을 때만 데이터 추가
                if sub_definitions and sub_examples:
                    extracted_data.append({
                        'definitions': sub_definitions,
                        'examples': sub_examples
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
        # print(audio)
        extracted_data.append({
            'audioFile': audio
        })

    # 추출한 데이터 출력
    print(json.dumps(extracted_data, indent=2))
    print("===============================")
    print(extracted_data)

    # 데이터를 pandas DataFrame으로 변환
    df = pd.DataFrame(extracted_data)

    # 엑셀 파일로 저장
    df.to_excel('extracted_data2.xlsx', index=False)

    print("엑셀 파일로 저장되었습니다.")
else:
    print("No data found in 'results'.")
