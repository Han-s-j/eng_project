import json

with open('sample.json') as file:
    datas = json.load(file)

    json_test = datas['results']
    # print(json_test)
    for k in json_test:
        print(k)