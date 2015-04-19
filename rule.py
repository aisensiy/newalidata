#!/usr/bin/env python
# encoding: utf-8

from csv import DictReader
from collections import defaultdict
import pandas as pd

item_subset = set()

def in_range(day, day_range):
    return day_range[0] <= day <= day_range[1]

with open('items.txt') as f:
    for line in f:
        item_subset.add(line.strip())
print 'subset created'


def get_features(filepath, date_range, subset=None):
    last_train_day = date_range[-3:-1]
    train_day = [date_range[0], date_range[-2]]
    predict_day = date_range[-1]
    print 'predict_day: %s' % predict_day
    print 'train_day: %s' % ' '.join(train_day)
    print 'last_train_day: %s' % ' '.join(last_train_day)

    cart_set = defaultdict(int)
    total_buy_set = defaultdict(int)
    total_action_set = defaultdict(int)
    buy_set = defaultdict(int)
    action_set = defaultdict(int)
    trues = set()
    rows = {}
    with open(filepath) as f:
        reader = DictReader(f)
        for idx, row in enumerate(reader):
            if subset and row['item_id'] not in item_subset:
                continue

            date = row['time'].split(' ')[0]
            key = row['user_id'] + '_' + row['item_id']
            behavior = int(row['behavior_type'])

            # last_cart, last_buy, last_action, total_buy, label
            rows.setdefault(key, [0, 0, 0, 0, 0])
            if behavior ==  3 and in_range(date, last_train_day):
                rows[key][0] += 1

            if behavior == 4 and in_range(date, last_train_day):
                rows[key][1] += 1

            if in_range(date, last_train_day):
                rows[key][2] += 1

            if behavior == 4 and in_range(date, train_day):
                rows[key][3] += 1

            if behavior == 4 and date == predict_day:
                rows[key][4] = 1

            # if in_range(date, train_day):
            #     total_action_set[key] += 1

            if idx % 500000 == 0:
                print 'processed: [%d]' % idx

    df = pd.DataFrame(rows).T
    df.index.name = 'id'
    df.columns = ['cart',
                  'buy',
                  'action',
                  'total_buy',
                  'label']
    filename = '-'.join(map(lambda x: x[5:].replace('-', ''),
                            [train_day[0], predict_day])) + (subset and '_sub.csv' or '_all.csv')
    print 'save to ' + filename
    df.to_csv(filename)


if __name__ == '__main__':
    import sys
    rng = pd.date_range(start='2014-' + sys.argv[1], end='2014-' + sys.argv[2])
    rng = map(lambda x: x.strftime('%Y-%m-%d'), rng)
    get_features('tianchi_mobile_recommend_train_user.csv', rng,
                 sys.argv[3] == '1' and item_subset or None)
