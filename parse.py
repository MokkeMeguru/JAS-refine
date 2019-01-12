import re
import csv


def parse_line(line, c):
    raw_text = line[:-2]
    raw_label = line[-2]
    text = re.sub(r'http[^\s]*|pic[^\s]*|@[^▁]*|#[^▁]*', '',
                  raw_text.replace(' ', '')).replace('▁', ' ').replace(
                      ' ', '。').lstrip('。').replace('\t', '')
    return text, int(raw_label)


def parse(fname):
    csvfile = open(
        'raw_{}.csv'.format(fname.split('/')[-1].split('.')[0]),
        'w',
        encoding='utf-8')
    csvfilewriter = csv.writer(
        csvfile,
        lineterminator='\n',
        quoting=csv.QUOTE_NONNUMERIC,
        delimiter=',')
    with open(fname, 'r', encoding='utf-8') as f:
        c = -1
        for line in f:
            c += 1
            if not c == 0:
                text, label = parse_line(line, c)
                csvfilewriter.writerow([text, label])
    csvfile.close()


if __name__ == '__main__':
    fnames = ['JAS/dev.tsv', 'JAS/test.tsv', 'JAS/train.tsv']
    for fname in fnames:
        parse(fname)
