import os
import pickle

from sklearn.utils import shuffle
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import *
import re
from bs4 import BeautifulSoup


class Utils:
    """
    Class containing methods that serve as helper functions
    """

    def shuffle_data(self, data_pd):
        """
        Data shuffling
        """

        data_columns = data_pd.columns
        data_body = data_pd[data_columns]
        data_body = shuffle(data_body)

        return data_body

    def string_to_words(self, query):
        """
        from string of words to list of processed words
        """

        nltk.download("stopwords", quiet=True)
        try:
            # add_similar_words_to_search_query(query[-1])
            text = BeautifulSoup(query[-1], "html.parser").get_text()  # Remove HTML tags
            text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())  # Remove non-alphanumeric and Convert to lower case
        except:
            text = ''
        word_list = text.split()  # Split string into words
        word_list = [w for w in word_list if w not in stopwords.words("english")]  # Remove stopwords
        word_list = [PorterStemmer().stem(w) for w in word_list]  # stem

        return [query[0], word_list]

    def clean_data(self, data, cache_dir, cache_file="cleaned_data.pkl"):
        """
        Convert each data row to words; read from cache if available.
        input: dataframe with columns key->col1, value->col2
        output: list of lists, e.g [[employee1_id,body1_word_list],[employee2_id,body2_word_list],...]
        """

        data_keys, data_body = data[data.columns[0]].values, data[data.columns[1]].values
        data_train = [[data_keys[i], data_body[i]] for i in range(len(data_body))]

        # If cache_file is not None, try to read from it first
        cache_data = None
        if cache_file is not None:
            try:
                with open(os.path.join(cache_dir, cache_file), "rb") as f:
                    cache_data = pickle.load(f)
                print("Read cleaned data from cache file:", cache_file)
            except:
                pass  # unable to read from cache, but that's okay

        # If cache is missing, then do the heavy lifting
        if cache_data is None:
            # Preprocess the data to obtain words for each employee data
            words_train = list(map(self.string_to_words, data_train))

            # Write to cache file for future runs
            if cache_file is not None:
                cache_data = dict(words_train=words_train)
                with open(os.path.join(cache_dir, cache_file), "wb") as f:
                    pickle.dump(cache_data, f)
                print("Wrote preprocessed data to cache file:", cache_file)
        else:
            # Unpack data loaded from cache file
            words_train = (cache_data['words_train'])

        return words_train

    def add_data_to_pickle(self, data_file, data=None, path='./'):

        data_path = path + data_file

        data_file_name = data_file.split('.')[0]
        pickle_file_name = path + 'data_dict.pkl'

        if os.path.isfile(pickle_file_name):
            pickle_file = open(pickle_file_name, 'rb')
        else:
            pickle_file = open(pickle_file_name, 'bw')
            pickle_file.close()

        if os.path.getsize(pickle_file_name) > 0:
            data_collections = pickle.load(pickle_file)
            pickle_file.close()
        else:
            data_collections = {}

        data_collections[data_file_name] = data
        with open(pickle_file_name, 'bw') as f:
            pickle.dump(data_collections, f)

    def swap_key_value(self, index_id):
        return {emm_id: index for index, emm_id in index_id.items()}

    def resume_index_id_data(self, data_processed_with_id):
        count, index_id, data = 0, {}, []
        for item in data_processed_with_id:
            index_id[count] = item[0]
            data.append(item[1])
            count += 1
        return index_id, data
