import glob
import os
import shutil
import pandas as pd

from tika import parser
import textract

from Production.Utils import Utils


class RecruitmentPreprocess:

    def __init__(self, resume_path, save_to_path=None):
        """
        Preprocesses document text queries.
        :param resume_path: str
        :param save_to_path: str
        """

        self.resume_path = resume_path

        if save_to_path is not None:
            self.save_to_path = save_to_path
            self.resume_id_data, self.resume_count, self.resume_id_index, self.resume_id_data, self.resume_data = self.__merge_resume_to_dataframe()

    def extract_text_from_resume(self, file_name):
        """
        Converts documents to text
        :param file_name: str
        :return: str
        """
        if file_name.split('.')[-1] == "pdf":
            text = parser.from_file(self.resume_path + file_name)['content']
        elif file_name.split('.')[-1] in ["doc", "docx", "txt"]:
            text = textract.process(self.resume_path + file_name).decode()
        else:
            text = ""
        return text

    def __merge_resume_to_dataframe(self):
        """
        Applies extract_text_from_resume to all files in the folder
        :return: tuple
        """

        all_collection = []
        all_files = [file.split('\\')[-1] for file in glob.glob(self.resume_path + "*") if not file.startswith('~')]
        index = 1
        resume_id_index = {}
        resume_id_data = {}

        for file in all_files:
            if file.split('.')[-1] in ['docx', 'pdf', 'doc']:
                resume_id_index[index] = '{}_{}'.format(''.join(file.split('.')[:-1]), index)
                resume_id_data[index] = self.extract_text_from_resume(file)
                collection = [index, self.extract_text_from_resume(file)]
                all_collection.append(collection)
                index += 1

        return resume_id_data, index-1, resume_id_index, resume_id_data, pd.DataFrame(all_collection, columns=['employee_id', 'data'])

    def save_resume_data_to_csv(self):
        """
        Saves dataframe to csv readable file
        :return: None
        """

        self.resume_data.to_csv(self.save_to_path + 'resume_data.csv', index=False)

    def add_resume_data_to_pickle(self):
        """
        Adds document data with corresponding id to pickle file
        :return: None
        """

        utils = Utils()
        utils.add_data_to_pickle('resume_id_data', self.resume_id_data, self.save_to_path)

    def add_resume_count_to_pickle(self):
        """
        Add the total number of documents to pickle file
        :return: None
        """

        utils = Utils()
        utils.add_data_to_pickle('resume_count', self.resume_count, self.save_to_path)

    def add_resume_keys_to_pickle(self):
        """
        Add the dict of index and id of document to pickle file
        :return: None
        """

        utils = Utils()
        utils.add_data_to_pickle('resume_id_index', self.resume_id_index, self.save_to_path)

    def add_user_accessible_resume_to_pickle(self):
        """
        Add the raw unprocessed document data to pickle file
        :return: None
        """

        utils = Utils()
        utils.add_data_to_pickle('user_accessible_resume', self.resume_id_data, self.save_to_path)

    def add_processed_resume_to_pickle(self):
        """
        Add the processed document data to pickle file
        :return: None
        """

        cache_directory = os.path.join("cache", "words_tokens")  # where to store cache files
        os.makedirs(cache_directory, exist_ok=True)  # ensure cache directory exists

        cache_file = 'cleaned_{}.pkl'.format('processed_resume')

        utils = Utils()

        data_shuffled = utils.shuffle_data(self.resume_data)
        data_processed_with_id = utils.clean_data(data_shuffled, cache_directory, cache_file=cache_file)

        shutil.rmtree('cache')

        utils.add_data_to_pickle('processed_resume', data_processed_with_id, self.save_to_path)
