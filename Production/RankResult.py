import os
import pickle

from Production.ModelScores import ModelScores
path_to = "Data/Workin_Data/"


class RankResult:

    def __init__(self, no_of_output, resume_words_counts, model):
        """
        Extracts documents using scores from the ranking algorithms and formats appropriately
        :param no_of_output: int
        :param resume_words_counts: int
        :param model: str
        """

        with open(path_to + 'data_dict.pkl', 'rb') as f:
            pickle_data = pickle.load(f)
        self.user_accessible_resume = pickle_data['resume_id_index']
        self.resume_id_data = pickle_data['resume_id_data']
        self.no_of_output = no_of_output
        self.resume_words_counts = resume_words_counts
        self.model_scores = ModelScores()
        self.model = model

    def get_ranking_with_resume_id(self, resume_id):
        """
        Gets the documents based on the scores from the ranking algorithm using resume id
        :param resume_id: int
        :return: list
        """

        scores = self.model_scores.get_resume_id_ranking_scores(resume_id, self.model)
        ranked_resume_names = []

        for i in range(self.no_of_output):
            if i >= len(scores):
                break
            ranked_resume_names.append([self.user_accessible_resume[scores[i][0]], " ".join(self.resume_id_data[scores[i][0]].split(" ")[:self.resume_words_counts])])

        return ranked_resume_names

    def get_ranking_with_query(self, query):
        """
        Gets the documents based on the scores from the ranking algorithm using search query
        :param query: str
        :return: list
        """

        if query is None or query.strip() == "":
            return None

        scores = self.model_scores.single_query_scores(query, self.model)
        ranked_resume_names = []

        for i in range(self.no_of_output):
            if i >= len(scores):
                break
            ranked_resume_names.append([self.user_accessible_resume[scores[i][0]], " ".join(self.resume_id_data[scores[i][0]].split(" ")[:self.resume_words_counts])])

        return ranked_resume_names

