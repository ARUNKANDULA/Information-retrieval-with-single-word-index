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
