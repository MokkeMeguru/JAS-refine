import csv
import json
import requests
import urllib3
import yaml


def generate_concat_file():
    fnames = [
        'raw_train.csv',
        'raw_test.csv',
        'raw_dev.csv'
    ]
    texts = []
    labels = [0, 0, 0, 0, 0, 0]
    for fname in fnames:
        with open('bakup/raw-data/{}'.format(fname),
                  'r', encoding='utf-8') as f:
            csvlines = csv.reader(f, csv.QUOTE_NONNUMERIC)
            for row in csvlines:
                texts += row[0] + '\n'
                labels[int(row[1])] += 1

    print('[INFO] labale\n0:{} 1:{} 2:{} 3:{} 4:{} 5:{}'
          .format(labels[0], labels[1], labels[2],
                  labels[3], labels[4], labels[5]))
    with open('{}'.format('raw.txt'),
              'w', encoding='utf-8') as f:
        f.writelines(texts)
    print('[INFO] generated\nPlease check "raw.txt"')


def post(api_key, data):
    url = 'https://language.googleapis.com/v1/documents:analyzeSentiment?key={}'.format(api_key)
    headers = {
        'Content-Type': 'application/json'
    }
    body = {
        "encodingType": "UTF8",
        "document": {
            "type": "PLAIN_TEXT",
            "language": "ja",
            "content": data
        }
    }
    r = requests.post(url=url, headers=headers, json=body)
    r.encoding = r.apparent_encoding
    return r.json()


def retagging():
    with open('config_secret.yaml', 'r', encoding='utf-8') as f:
        config = yaml.load(f)
    with open('raw.txt', 'r', encoding='utf-8') as f, \
            open('retagged-sentence.csv', 'w', encoding='utf-8', newline='') as wsent, \
                open('retagged-raw.csv', 'w', encoding='utf-8', newline='') as wraw:
        csvwsent = csv.writer(wsent, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        csvwraw = csv.writer(wraw, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        csvwsent.writerow(['idx', 'sentence', 'magnitude', 'score'])
        csvwraw.writerow(['idx', 'text', 'magnitude', 'score'])
        idx = -1
        for line in f:
            idx += 1
            data = line[:-1]
            api_key = config['GCP']['API-key']
            try:
                r = post(api_key, data)
                csvwraw.writerow([idx, data,
                                  float(r['documentSentiment']['magnitude']),
                                  float(r['documentSentiment']['score'])])
                for info in r['sentences']:
                    csvwsent.writerow([idx, info['text']['content'],
                                       float(info['sentiment']['magnitude']),
                                       float(info['sentiment']['score'])])
            except Exception:
                pass


if __name__ == '__main__':
    generate_concat_file()
    retagging()
