"""
This is a comand-line script to retrieve articles from Amcat and dump them
to either txt or json files.
"""
import amcatclient
import sys
from tqdm import tqdm
import math
import json
import os
import argparse

conn = amcatclient.AmcatAPI("https://vu.amcat.nl")


def get_articles(id_list, project, articleset, batch_size=100,
                 nr_articles=None, max_date=None, min_date=None):
    i = 0
    if nr_articles is None:
        nr_articles = len(id_list)
    for batch in range(math.ceil(nr_articles/batch_size)):
        id_list_sub = id_list[batch*batch_size:batch*batch_size+batch_size]
        articles = conn.get_articles_by_id(articles=id_list_sub,
                                           project=project,
                                           articleset=articleset,
                                           columns='date,title,text')
        for art in articles:
            if max_date is None or art['date'] <= max_date:
                if min_date is None or art['date'] >= min_date:
                    if i < nr_articles:
                        yield art
                        i += 1


def get_article_ids(project, articleset):
    articles_ids = [a['id'] for a in conn.get_articles(
        project=project, articleset=articleset, columns=[])]
    return articles_ids


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output_dir', default=os.path.curdir)
    parser.add_argument('-n', '--nr_docs', type=int, default=None)
    parser.add_argument('-b', '--batch_size', type=int, default=100)
    parser.add_argument('-p', '--project', type=int, default=69)
    parser.add_argument('-a', '--articleset', type=int, default=None)
    parser.add_argument(
        '-f', '--format', choices=['json', 'txt'], default='json')
    parser.add_argument('-max', '--max_date', type=str, default=None,
                        help='max date in format 2021-03-17T00:00:00')
    parser.add_argument('-min', '--min_date', type=str, default=None,
                        help='min date in format 2021-03-17T00:00:00')
    parser.add_argument('-v', '--verbose', action='store_true')
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    article_ids = []
    for art_id in get_article_ids(args.project, args.articleset):
        if not os.path.exists(os.path.join(args.output_dir, '{}.json'.format(art_id))):
            article_ids.append(art_id)
    print('Nr of articles: {}'.format(len(article_ids)))
    articles = get_articles(article_ids, args.project, args.articleset,
                            args.batch_size, args.nr_docs, args.max_date, args.min_date)
    for a in tqdm(articles, total=args.nr_docs):
        if args.format == 'json':
            with open(os.path.join(args.output_dir, '{}.json'.format(a['id'])), 'w') as fout:
                json.dump({
                    'id': a['id'],
                    'title': a['title'],
                    'text': a['text']}, fout)
        else:
            with open(os.path.join(args.output_dir, '{}.txt'.format(a['id'])), 'w') as fout:
                fout.write(a['text'])
