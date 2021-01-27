import pickle
from operator import itemgetter

from Production.Utils import Utils
from Production.models.BM25 import BM25
from Production.models.BM25Adpt import BM25Adpt
from Production.models.BM25L import BM25L
from Production.models.BM25Okapi import BM25Okapi
from Production.models.BM25Plus import BM25Plus
from Production.models.BM25T import BM25T


class ModelScores:

    def __init__(self):
        """
        Returns Model Scores for single query, single resume and for all resumes
        """

        with open('Data/Workin_Data/' + 'data_dict.pkl', 'rb') as f:
            self.pickle_data = pickle.load(f)

        self.utils = Utils()

    def get_resume_id_ranking_scores(self, resume_id, model):
        """
        Returns Model Scores for single resume
        :param resume_id: int
        :param model: str
        :return: list[list]
        """

        user_accessible_resume = self.pickle_data['user_accessible_resume']
        processed_resume = self.pickle_data['processed_resume']

        data_index_resume_id, data_processed = self.utils.resume_index_id_data(processed_resume)

        # Remove the resume from the list of resumes to be compared to
        data_processed_copy = data_processed[:]
        index = self.utils.swap_key_value(data_index_resume_id)[resume_id]
        del data_processed_copy[index]

        raw_query = user_accessible_resume[resume_id]

        if model == 'BM25Okapi':
            chosen_model = BM25Okapi(data_processed_copy)
        elif model == 'BM25L':
            chosen_model = BM25L(data_processed_copy)
        elif model == 'BM25Adpt':
            chosen_model = BM25Adpt(data_processed_copy)
        elif model == 'BM25T':
            chosen_model = BM25T(data_processed_copy)
        else:
            chosen_model = BM25Plus(data_processed_copy)

        scores = list(chosen_model.get_scores(self.utils.string_to_words(['', raw_query])[-1]))

        scores.insert(index, float('inf'))
        indices, id_sorted = zip(*sorted(enumerate(scores), reverse=True, key=itemgetter(1)))

        return [[data_index_resume_id[indices[i]], id_sorted[i]] for i in range(0, len(indices))][1:]

    def single_query_scores(self, query, model):
        """
        Returns Model Scores for single query
        :param query: str
        :param model: str
        :return: list[list]
        """

        if query.strip() == "":
            return None

        processed_resume = self.pickle_data['processed_resume']
        data_index_employee_id, data_processed = self.utils.resume_index_id_data(processed_resume)

        if model == 'BM25':
            chosen_model = BM25(data_processed)
        elif model == 'BM25Okapi':
            chosen_model = BM25Okapi(data_processed)
        elif model == 'BM25L':
            chosen_model = BM25L(data_processed)
        elif model == 'BM25Adpt':
            chosen_model = BM25Adpt(data_processed)
        elif model == 'BM25T':
            chosen_model = BM25T(data_processed)
        else:
            chosen_model = BM25Plus(data_processed)

        scores = list(chosen_model.get_scores(self.utils.string_to_words(['', query])[-1]))
        indices, id_sorted = zip(*sorted(enumerate(scores), reverse=True, key=itemgetter(1)))

        return [[data_index_employee_id[indices[i]], id_sorted[i]] for i in range(len(indices))]
