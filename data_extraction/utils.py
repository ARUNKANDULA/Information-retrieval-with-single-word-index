import regex as re

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
    
data_extraction = DataExtraction()