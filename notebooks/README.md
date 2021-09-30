## Notebooks for issue detection
The aim of these notebooks is to expand a manually crafted set of query terms for a list of issues, using a word embedding model. We use a fasttext model with dimension 50, trained on the AEM corpus and material from ACMAT up to december 2020.


### Step 1: expand wildcards
Some query words contain wildcards (asterices). We use the vocabulary of the word embedding model to find all words that match the wildcard. This is done in the notebook [Issues_expand_wildcards.ipynb](https://github.com/Filter-Bubble/stance_finder/blob/main/notebooks/Issues_expand_wildcards.ipynb). We save a table with all query terms, including whether they were original or resulted from the expansion. We also include the original query terms with wildcards.

Note that the number of wildcard queries varies per issue, and for some issues the expanded set is very large. This means there is likely many false positives in the expanded set for this issues. We also see that there is some query terms that appear in multiple issues.

We also need to preprocess all words similar to the word embedding model. This means lowercasing, and removing all non-alphabetical characters. Note that some queries become more difficult to interpret after this preprocessing.

### Step 2: explore networks of embedding neighbors
The query sets that result from step 1 are explored in the notebook [Issues-explore-embedding.ipynb](https://github.com/Filter-Bubble/stance_finder/blob/main/notebooks/issues-explore-embedding.ipynb). We look up all queries in the embedding model and look at the similarities between query terms. If a query consists of multiple words, we use the average of the embeddings of the individual word.

The first set of visualizations explore the distribution of similarities. This reveils how coherent the query sets are for each issue.

We also draw networks of the pairwise similarities between the query terms (only for the issues with smaller query sets). These network could be used to more quickly clean the set of query terms (e.g. by removing clusters of falsely expanded words that are not related to the issue). We save the networks to `.gexf` files so they can be loaded into Gephi.

Lastly, we explore, for one issue, networks where we include the nearest neighbors to the query terms.We can experiment with the number of neighbors and the cut-off value we choose to define edges.


### Step 3: expand query set with cross validation
In the previous exploratory notebook, we choose a few issues for which the query set seems clean.
For these issues, we expand the query sets with the nearest neighbors in the word embedding model, see [Query_set_expansion_CV_subset.ipynb](https://github.com/Filter-Bubble/stance_finder/blob/main/notebooks/Query_set_expansion_CV_subset.ipynb). We do this in a cross validated manner, where in each fold, we take a different subset of the query set as seed set, and take the nearest neighbors of the centroid of the embeddings of this seed set. The rest of the query set is used for estimating precision and recall.

### Step 4: Export top-n neighbor sets
From the notebook in step 3, we make decisions on how many neighbors to include in the expanded query set. We make this decision based on the elbows in the recall graph. The top-n neighbors for these issues are exported in in [Export_ranked_neighbors.ipynb](https://github.com/Filter-Bubble/stance_finder/blob/main/notebooks/Export_ranked_%20neighbors.ipynb).