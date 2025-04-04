import json
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
            # audioFile 추출
            audio_files = [pronunciation.get('audioFile') for pronunciation in sense.get('pronunciations', []) if pronunciation.get('audioFile')]

            # definitions 또는 examples가 비어 있으면 None으로 처리
            if not definitions:
                definitions = None
            if not examples:
                examples = None
            if not audio_files:
                audio_files = None

            # definitions, examples, audio_files이 하나라도 존재할 때만 추가
            if definitions or examples or audio_files:
                extracted_data.append({
                    'definitions': definitions[0] if definitions else None,  # 첫 번째 정의만 사용
                    'examples': examples[0] if examples else None,  # 첫 번째 예시만 사용
                    'audio_files': ', '.join(audio_files) if audio_files else None  # 오디오 파일 URL들 합치기
                })

            # subsenses 처리
            subsenses = sense.get('subsenses', [])
            for subsense in subsenses:
                sub_definitions = subsense.get("definitions", [])
                sub_examples = [example.get('text') for example in subsense.get('examples', [])]
                sub_audio_files = [pronunciation.get('audioFile') for pronunciation in subsense.get('pronunciations', []) if pronunciation.get('audioFile')]

                # subsense의 definitions 또는 examples가 비어 있으면 None으로 처리
                if not sub_definitions:
                    sub_definitions = None
                if not sub_examples:
                    sub_examples = None
                if not sub_audio_files:
                    sub_audio_files = None

                # subsense의 정의, 예시, 오디오 파일이 있을 경우에만 추가
                if sub_definitions or sub_examples or sub_audio_files:
                    extracted_data.append({
                        'definitions': sub_definitions[0] if sub_definitions else None,  # 첫 번째 정의만 사용
                        'examples': sub_examples[0] if sub_examples else None,  # 첫 번째 예시만 사용
                        'audio_files': ', '.join(sub_audio_files) if sub_audio_files else None  # 오디오 파일 URL들 합치기
                    })

    # 데이터를 pandas DataFrame으로 변환
    df = pd.DataFrame(extracted_data)

    # 데이터가 있을 때만 엑셀 파일로 저장
    if not df.empty:
        df.to_excel('extracted_data_with_audio2.xlsx', index=False)
        print("엑셀 파일로 저장되었습니다.")
    else:
        print("빈 데이터가 없어 엑셀로 저장할 수 없습니다.")
else:
    print("No data found in 'results'.")
