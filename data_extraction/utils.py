import json
import numpy as np
import regex as re
import pandas as pd

class DataExtraction():
    def __init__(self):
        pass


    def extract_text_between_tags(self, doc, tag) -> str:
        '''
        inputs:
            - doc: string of individual html doc
            - tag: name of the tag between which the text should be extracted

        output:
            - string of extracted text
        '''
        start_tag = f'<{tag}>'  # opening tag
        end_tag = f'</{tag}>'   # closing tag
        start_index = 0

        while True:
            start_index = doc.find(start_tag, start_index)
            if start_index == -1:
                break
            start_index += len(start_tag)
            end_index = doc.find(end_tag, start_index)
            if end_index == -1:
                break
            extracted_text = doc[start_index:end_index].strip()
            start_index = end_index + len(end_tag)

        return extracted_text
    
    def extract_text_in_tag(self, doc, tag) -> str:
        '''
        inputs:
            - doc: string of individual html doc
            - tag: name of the tag between which the text should be extracted

        output:
            - string of extracted text
        '''
        start_tag = f'<{tag}>'  # opening tag
        end_tag = f'<'   # closing tag
        start_index = 0

        while True:
            start_index = doc.find(start_tag, start_index)
            if start_index == -1:
                break
            start_index += len(start_tag)
            end_index = doc.find(end_tag, start_index)
            if end_index == -1:
                break
            extracted_text = doc[start_index:end_index].strip()
            start_index = end_index + len(end_tag)

        return extracted_text

    def tokenizer(self, text, stopwords_list) -> list:
        # excluding numbers and any words that contain numbers in the provided text
        cleaned_text = re.sub(r'\b\w*\d\w*\b', '', text)
        # removing any extra spaces between words that was created after excluding numbers from above line 
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()    # removing any leading or trailing spaces with .strip()
        # split on all nonalphanumeric characters
        words = re.split(r'\W+', cleaned_text)
        # removing any empty strings created after splitting and converting all the words to lower case
        words = [word.lower() for word in words if word]
        # soring all the words
        words = sorted(words)
        # removing stop words
        words = [word for word in words if word not in stopwords_list]

        # eliminating duplicate words in the list
        unique_words = list(set(words))
        
        return words, unique_words
    
    def load_json_file(self, path):
        with open(path) as file:
            json_data = json.load(file)
        return json_data
    
    def get_forward_index(self, stemmed_words):
        unique_stemmed_words = list(set(stemmed_words))
        forward_index = {}
        for unique_word in unique_stemmed_words:
            count = stemmed_words.count(unique_word)
            forward_index[unique_word] = count
        return forward_index, unique_stemmed_words
    
    def sort_df_and_add_sequence(self, df):
        df = df.sort_values(by=['Topic', 'Cosine_value'], ascending=[True, False])
        df.insert(2, 'Sequence', 0)
        topics = df['Topic'].unique()
        counter = 1
        for current_topic in topics:
            for index, row in df.iterrows():
                if row['Topic'] != current_topic:
                    current_topic = row['Topic']
                    counter = 1
                df.at[index, 'Sequence'] = counter
                counter += 1
        df.reset_index(drop=True, inplace=True)
        return df
    
    def compare_retrieved_docs_wt_gt(self, retrieved_docs, ground_truth):
        retrieved_docs['Topic'] = retrieved_docs['Topic'].astype(int)
        ground_truth['Topic'] = ground_truth['Topic'].astype(int)
        
        avaliable_topics = list(map(int, retrieved_docs['Topic'].unique()))
        # Extract ground truth only for avalable topics
        ground_truth = ground_truth[ground_truth['Topic'].isin(avaliable_topics)]

        # Adding relevance column in the dataframe. If Cosine_value is > 0 then Relecance is considered 1 else 0
        retrieved_docs['Relevance'] = np.where(retrieved_docs['Cosine_value'] > 0, 1, 0)

        # Merge the DataFrames
        merged_df = pd.merge(retrieved_docs, ground_truth, on=['Topic', 'Document'], suffixes=('_res', '_gt'), how='left', indicator=True)

        # Contains documents that retrieval matched the ground truth
        matched_df_v1 = merged_df[merged_df['_merge'] == 'both']
        # Contains documents that retrieval did not match ground truth
        not_matched_df_v1 = merged_df[merged_df['_merge'] == 'left_only']

        true_positives = len(matched_df_v1[matched_df_v1['Relevance_res'] == 1])
        true_negatives = len(matched_df_v1[matched_df_v1['Relevance_res'] == 0])

        false_positives = len(not_matched_df_v1[not_matched_df_v1['Relevance_res'] == 1])
        false_negatives = len(not_matched_df_v1[not_matched_df_v1['Relevance_res'] == 0])

        return(true_positives, true_negatives, false_positives, false_negatives)
    
data_extraction = DataExtraction()