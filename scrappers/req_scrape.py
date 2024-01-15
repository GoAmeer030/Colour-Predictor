import requests
import json

import pandas as pd

import os
import threading
import dotenv

dotenv.load_dotenv()

URL = os.getenv('REQ_SCRAPPER_URL')
HEADER = {'Token': os.getenv('TOKEN')}

jsons = []
datas = []


def scrape(p_id):
    j = []
    try:
        flag = 1
        page = 1
        last_len = 0

        while flag:
            PAYLOAD = {'project_id': p_id + 1, 'page': page, 'count': 10}

            r = requests.post(URL, headers=HEADER, data=PAYLOAD)
            j.append(json.loads(r.content)['data']['game_history']['list'])

            jlen = len(j)
            print(f"{p_id + 1}: {page}: {r}: {jlen}")
            page += 1

            if (r.status_code != 200) or (jlen == last_len) or len(j[-1]) == 0:
                flag = 0

            last_len = jlen
    except Exception as e:
        print(e)
        flag = 0

    jsons.append(j)


# Multi-threading for faster scraping
threads = []
for p_id in range(4):
    t = threading.Thread(target=scrape, args=(p_id,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

for project_list in jsons:
    for json in project_list:
        for data in json:
            date = data['date']
            sn = data['sn']
            price = data['price']
            project_id = int(data['project_id']) - 1
            unit = data['unit']
            begintime = data['begintime']

            color = data['color']
            if len(color) > 5:
                color = color.split(',')
                color = color[0]

            if color == 'red':
                color = 0
            elif color == 'green':
                color = 1
            else:
                raise Exception('Not a Valid Colour')

            datas.append([date, sn, price, project_id, begintime, unit, color])

df = pd.DataFrame(datas, columns=['period', 'sn', 'price', 'project_id', 'begintime', 'target_number', 'target_colour'])

# check for raw_data.csv if exists append the data else create a new file
if os.path.exists('../dataset/raw_data.csv'):
    df.to_csv('../dataset/raw_data.csv', mode='a', header=False, index=False)
else:
    df.to_csv('../dataset/raw_data.csv', index=False)
