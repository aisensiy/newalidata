#!/usr/bin/env python
# encoding: utf-8

from sklearn.ensemble import RandomForestClassifier
import pandas as pd


def train(train_df, test_df, cnt=200, test=True):
    test_trues = set(test_df[test_df.label == 1]['id'].tolist())
    clf = RandomForestClassifier(n_estimators=10)
    clf.fit(train_df.values[:, 1:-1], train_df.values[:, -1])
    pred = clf.predict_proba(test_df.values[:, 1:-1])
    y_pred = pd.DataFrame({'id': test_df['id'].tolist(), 'proba': pred[:, 1], 'label': test_df['label']})
    y_pred.sort_index(by='proba', ascending=False, inplace=True)

    r_count = len(y_pred[y_pred.label == 1])
    if test:
        pred_result = y_pred.head(cnt)
        p_count = len(pred_result[pred_result.label == 1])
        p = p_count / float(cnt)
        r = p_count / float(r_count)
        print p_count
        print p
        print r
        print 2 * p * r / (p + r)
    return y_pred


def make_submission(pred_df, filepath, cnt):
    pred_df['user_id'] = pred_df['id'].map(lambda x: x.split('_')[0])
    pred_df['item_id'] = pred_df['id'].map(lambda x: x.split('_')[1])
    print pred_df
    result = pred_df[['user_id', 'item_id']]
    result.head(cnt).to_csv(filepath, index=None)


if __name__ == '__main__':
    import sys
    train_df = pd.read_csv(sys.argv[1])
    test_df = pd.read_csv(sys.argv[2])
    if len(sys.argv) >= 5:
        y_pred = train(train_df, test_df, int(sys.argv[3]), False)
        make_submission(y_pred, sys.argv[4], int(sys.argv[3]))
    else:
        y_pred = train(train_df, test_df, int(sys.argv[3]), True)
