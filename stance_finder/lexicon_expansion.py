"""
This is an attempt to implement a simplified version of Amslers lexicon expansion algorithm.
Amslers implementation can be found at https://github.com/remamsler/LexExpander

Reference:  Michael Amsler - "Using Lexical-Semantic Concepts
for Fine-Grained Classification in the Embedding Space" (PhD Thesis)
"""

import fasttext
import collections
import numpy as np
from tqdm import tqdm


class FasttextNN:
    "Code largely taken from https://github.com/facebookresearch/fastText/issues/384"

    def __init__(self, model):
        self.model = model
        self.words = model.get_words()
        self.word_vectors = np.array([model[w] for w in self.words])

    def get_nearest_neighbors(self, seed_set, k=10, exclude_seedset=True):
        query = np.sum([self.model[w] for w in seed_set], axis=0)
        norms = np.sqrt((query**2).sum() * (self.word_vectors**2).sum(axis=1))
        cossims = np.matmul(self.word_vectors, query) / norms
        n_to_sort = k
        if exclude_seedset:
            n_to_sort += len(seed_set)
        rank = range(len(cossims)-n_to_sort, len(cossims))
        result_idx = np.argpartition(cossims, rank)[-n_to_sort:][::-1]
        result = [(cossims[idx], self.words[idx])
                  for idx in result_idx
                  if self.words[idx] not in seed_set or not exclude_seedset]
        if exclude_seedset:
            result = result[:k]
        return result


def resample(scores_and_words, topn, choosek):
    scores, candidates = zip(*scores_and_words)
    top_scores = np.argsort(scores)[-topn:]
    sample_idx = np.random.choice(top_scores, choosek)
    return list(np.array(candidates)[sample_idx])


def iterative_lexicon_expansion(fasttext_model, seed_terms, nnmodel=None,
                                nr_iterations=10, k=50, exclusion=[],
                                samplesize_lex=(1, 4),
                                samplesize_nonlex=(1, 2),
                                filter_to=100):
    '''
    Reference:  Michael Amsler - "Using Lexical-Semantic Concepts
    for Fine-Grained Classification in the Embedding Space" (PhD Thesis)

    '''
    if nnmodel is None:
        nnmodel = FasttextNN(fasttext_model)

    final_candidates = []
    new_seedterms = seed_terms
    for i in tqdm(range(nr_iterations)):
        most_similar = nnmodel.get_nearest_neighbors(new_seedterms,
                                                     k=50,
                                                     exclude_seedset=False)
        in_lex = []
        not_in_lex = []
        for candidate_score, candidate in most_similar:
            if candidate in exclusion:
                break
            elif candidate in seed_terms:
                in_lex.append((candidate_score, candidate))
            else:
                not_in_lex.append((candidate_score, candidate))
        final_candidates.extend([w for _, w in not_in_lex])
        new_seedterms = resample(in_lex, *samplesize_lex) + resample(not_in_lex, *samplesize_nonlex)

    final_candidates_agg = collections.Counter(final_candidates)
    filtered_candidates, _ = zip(*final_candidates_agg.most_common(filter_to))
    return filtered_candidates
