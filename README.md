# Information Retrieval CSCE5200
This is a project for the Information Retrieval class, aimed at building a search engine to retrieve documents based on a user query.

## Installation
```bash
# Navigate to the project directory
cd information_retrieval_CSCE5200

# Install dependencies
pip install -r requirements.txt
```

## Token Extraction from Source Documents
The Jupyter notebook to iterate through the entire dataset and save the tokens and document IDs as a text file is available in `notebooks/data_extraction.ipynb`. Run all the cells in that notebook to save all the unique tokens to a text file.


## Creating Forward and Inverted Index
Open `notebooks/index_construction.ipynb` and run all the cells in that notebook to create forward index and inverted index.
* Forward index is constructed in the following format:
```python
{
docID1: {wordIDi: freq in docID1; wordIdi+1: freq in docID1;...},
docID2: {wordIdj: freq in docID2; wordIdj+1: freq in docID2;...},
...
...
}
```


* Inverted index is constructed in the following format:
```python
{
wordID1: {docId1: freq in docID1, docId2: freq in docID2,...},
wordID2: {docId10: freq in docID10, docId12: freq in docID12,...},
...
...
}
```

*To test this forward and inverted index construction on test data set, change the data_path to `../test_data`*
<p align="center">
  <img src="images/dataset_path.png" />
</p>

## Query Retrieval and Performance Analysis
Code for this topic is in `notebooks/information_retrieval.ipynb`

Queries used in this project are in `input_query/topics.txt`. Each query is structured as the below screen shot.
<p align="center">
  <img src="https://github.com/user-attachments/assets/9fb36301-71ae-4218-8b2b-813640af987d" />
</p>

Each topic is contained within the `<top>` and `</top>` tags. The format of each query is as follows:
```
<num> Unique Query Number
<title> Main Query (Max. three words)
<desc> One sentence description of the query
<narr> Concise description of what makes a document relevant
```
Pseudo code for retrieving relevant documents and calculating the similarity
```
Split_topics_document_per_query():
   Iterate_over_each_query:
      query = extract_query_text()
      doc_ids = get_matched_documents_from_inverted_index(query)
      term_fwd_index = create_forward_index(query)
      for document in doc_ids:
         tf_idf_list = []
         query_freq_list = []
         for term in query:
            tf_idf = calculate_tf_idf_weight(term, document)
            query_freq = get_query_term_freq(term, query)
            
            append_to_list(tf_idf_list, tf_idf)
            append_to_list(query_freq_list, query_freq)
         
         tf_idf_vector = convert_list_to_vector(tf_idf_list)
         query_vector = convert_list_to_vector(query_freq_list)

         norm_tf_idf_vector = normalize_vector(tf_idf_vector)
         norm_query_vector = normalize_vector(query_vector)

         cosine_similarity = calculate_cosine_similarity(norm_tf_idf_vector, norm_query_vector)
         store_result(query, document, cosine_similarity)
```

**Performance Analysis**

The 'main.qrels' file consists of relevance judgements (manually judged) for each of the topics (queries) present in topics.txt file.

This file will be used to determine the performance of the system.

The format of the 'main.qrels' file is as follows:

`TOPIC`    `ITERATION`    `DOCUMENT`    `RELEVANCY` 

```
TOPIC is the topic number,
ITERATION is the feedback iteration (almost always zero and not used),
DOCUMENT is the document name that corresponds to the "docno" field in the documents, and
RELEVANCY is a binary code of 0 for not relevant and 1 for relevant.
```

Note that not all the documents are manually judged to find out if it is relevant/irrelevant to a topic. Hence, you can assume
that if the document name is not present in the file for any topic, then that document is irrelevant for our evaluations.
