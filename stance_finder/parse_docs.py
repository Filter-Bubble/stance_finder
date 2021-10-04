"""
This script is to retrieve articles from Amcat and parse them with the stanza
pipeline, including e2e-Dutch for coreference resolution and Stroll for semantic role labeling.
"""

import argparse
import amcatclient
import json
import os
from tqdm import tqdm
import logging
import glob
import unidecode
import stanza
import e2edutch.stanza
import stroll.stanza
import math

logger = logging.getLogger(__name__)


def get_articles(id_list, batch_size=100, nr_articles=None):
    i = 0
    if nr_articles is None:
        nr_articles = len(id_list)
    for batch in range(math.ceil(nr_articles/batch_size)):
        id_list_sub = id_list[batch*batch_size:batch*batch_size+batch_size]
        conn = amcatclient.AmcatAPI("https://vu.amcat.nl")
        articles = list(conn.get_articles_by_id(articles=id_list_sub,
                                                columns='date,title,text'))
        for art in articles:
            if i < nr_articles:
                yield art
            i += 1


def get_article_ids(project, articleset):
    conn = amcatclient.AmcatAPI("https://vu.amcat.nl")
    articles_ids = [a['id'] for a in conn.get_articles(
        project=project, articleset=articleset, columns=[])]
    return articles_ids


def filter_article_ids(article_ids, output_dir):
    # Exclude ids that already exist in output_dir
    filtered_article_ids = []
    for art_id in article_ids:
        output_filename = os.path.join(output_dir, '{}.json'.format(art_id))
        if not os.path.exists(output_filename):
            filtered_article_ids.append(art_id)
    return filtered_article_ids


def stanza_doc_to_dict(doc, doc_id='', title='', text=None):
    doc_dict = {'id': doc_id, 'title': title}
    if text is not None:
        doc_dict['text'] = text
    doc_dict['sentences'] = []
    for sent in doc.sentences:
        sent_list = []
        for word in sent.words:
            word_dict = {}
            word_dict.update(word.to_dict())
            word_dict['ner'] = word.parent.ner
            word_dict['srl'] = word.srl
            word_dict['frame'] = word.frame
            sent_list.append(word_dict)
        doc_dict['sentences'].append(sent_list)

    clusters_dict = [[span.to_dict() for span in cl] for cl in doc.clusters]
    doc_dict['clusters'] = clusters_dict
    return doc_dict


def preprocess(text):
    text = text.replace('„', '"')
    text = unidecode.unidecode(text)
    return text


def parse_docs(n, output_dir, batch_size, input_dir=None, project=None, articleset=None):
    if input_dir is None:
        article_ids = get_article_ids(project=project, articleset=articleset)
        article_ids = filter_article_ids(article_ids, output_dir)
        if n is None:
            n = len(article_ids)
        articles = get_articles(article_ids, nr_articles=n,
                                batch_size=batch_size)
        logger.info('Number of ids: {}'.format(len(article_ids)))
    else:
        articles = []
        for fname in glob.glob(os.path.join(input_dir, '*.json')):
            try:
                with open(fname) as fin:
                    art = json.load(fin)
                    articles.append(art)
            except Exception as e:
                logger.error('Error reading file {}'.format(fname))
                logger.error(e)
        logger.info('Number of articles: {}'.format(len(articles)))
        n = len(articles)
    # Create nlp pipeline
    nlp = stanza.Pipeline(lang='nl',
                          processors='tokenize,lemma,pos,depparse,srl,coref,ner')
    for art in tqdm(articles, total=n):
        try:
            output_filename = os.path.join(
                output_dir, '{}.json'.format(art['id']))
            if not os.path.exists(output_filename):
                text = preprocess(art['text'])
                doc = nlp(text)
                doc_dict = stanza_doc_to_dict(doc,
                                              doc_id=art['id'],
                                              title=art['title'],
                                              text=art['text'])
                with open(output_filename, 'w') as fout:
                    json.dump(doc_dict, fout)
            else:
                logger.info("Document {} already parsed".format(art['id']))
        except Exception as e:
            logger.error('Error with article {}'.format(
                art.get('id', 'UNKNOWN')))
            logger.error(e)
            # Refresh pipeline
            nlp = stanza.Pipeline(lang='nl',
                                  processors='tokenize,lemma,pos,depparse,srl,coref')


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output_dir', default=os.path.curdir)
    parser.add_argument('-i', '--input_dir', default=None)
    parser.add_argument('-n', '--nr_docs', type=int, default=None)
    parser.add_argument('-b', '--batch_size', type=int, default=100)
    parser.add_argument('-p', '--project', type=int, default=69)
    parser.add_argument('-a', '--articleset', type=int, default=None)
    parser.add_argument('-v', '--verbose', action='store_true')
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    if args.verbose:
        logger.setLevel(logging.INFO)
        logger.info("Set logging level to INFO")
    n = args.nr_docs

    parse_docs(n, args.output_dir, args.batch_size,
               args.input_dir, args.project, args.articleset)
