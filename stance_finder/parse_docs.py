import argparse
import amcatclient
import json
import os
from tqdm import tqdm

import stanza
import e2edutch.stanza
import stroll.stanza

conn = amcatclient.AmcatAPI("http://vu.amcat.nl")
project = 69
articleset = 2485
nr_docs = 12100


def get_n_articles(n=10):
    for i, a in enumerate(conn.get_articles(
            project=project,
            articleset=articleset,
            columns=['date', 'title', 'text'])):
        yield a

        if i >= n-1:
            break


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
            word_dict['srl'] = word.srl
            word_dict['frame'] = word.frame
            sent_list.append(word_dict)
        doc_dict['sentences'].append(sent_list)

    clusters_dict = [[span.to_dict() for span in cl] for cl in doc.clusters]
    doc_dict['clusters'] = clusters_dict
    return doc_dict


def parse_docs(n, output_dir):
    nlp = stanza.Pipeline(lang='nl',
                          processors='tokenize,lemma,pos,depparse,srl,coref')
    for art in tqdm(get_n_articles(n)):
        doc = nlp(art['text'])
        doc_dict = stanza_doc_to_dict(doc,
                                      doc_id=art['id'],
                                      title=art['title'],
                                      text=art['text'])
        output_filename = os.path.join(output_dir, '{}.json'.format(art['id']))
        with open(output_filename, 'w') as fout:
            json.dump(doc_dict, fout)


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output_dir', default=os.path.curdir)
    parser.add_argument('-n', '--nr_docs', type=int, default=None)
    parser.add_argument('-v', '--verbose', action='store_true')
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    if args.nr_docs is None:
        n = nr_docs
    else:
        n = args.nr_docs

    parse_docs(n, args.output_dir)
