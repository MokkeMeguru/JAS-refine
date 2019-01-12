import csv

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


def retagging():
    with open('config_secret.yaml', 'r', encoding='utf-8') as f:
        config = yaml.load(f)
    api_key = config['GCP']['API-key']

if __name__ == '__main__':
    generate_concat_file()
