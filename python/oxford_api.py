import json
import requests

app_id = "27b7e407"
app_key = "90833dce0340e245fa4e67934562a095"
endpoint = "entries" #sentences #entries
language_code = "en-us"
word_id = "about"

url = f"	https://od-api-sandbox.oxforddictionaries.com/api/v2/{endpoint}/{language_code}/{word_id.lower()}"
headers = {
    "app_id": app_id,
    "app_key": app_key
}

r = requests.get(url, headers=headers)

# 응답 코드 확인
print(f"Response code: {r.status_code}")

# 응답이 정상일 경우 JSON 데이터 출력
if r.status_code == 200:
    try:
        data = r.json()
        print(json.dumps(data, indent=4))  # 예쁘게 출력
    except ValueError:
        print("Response not in JSON format")
else:
    print(f"Error: {r.status_code}")
