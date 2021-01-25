import pickle

from Production.ModelScores import ModelScores
save_to_path = "./../Data/Workin_Data/"


class RankResult:

    def __init__(self, no_of_output, model):

        with open(save_to_path + 'data_dict.pkl', 'rb') as f:
            pickle_data = pickle.load(f)
        self.user_accessible_resume = pickle_data['resume_id_index']
        self.no_of_output = no_of_output
        self.model_scores = ModelScores()
        self.model = model

    def get_ranking_with_resume_id(self, resume_id):

        with open('./../Data/Workin_Data/' + 'data_dict.pkl', 'rb') as f:
            pickle_data = pickle.load(f)

        if resume_id is None or not(isinstance(resume_id, int)) or resume_id <= 0 or resume_id > pickle_data['resume_count']:
            return None

        scores = self.model_scores.get_resume_id_ranking_scores(145, self.model)
        ranked_resume_names = []

        for i in range(self.no_of_output):
            if i >= len(scores):
                break
            ranked_resume_names.append(self.user_accessible_resume[scores[i][0]])

        return ranked_resume_names

    def get_ranking_with_query(self, query):

        if query is None:
            return None

        scores = self.model_scores.single_query_scores(query, self.model)
        ranked_resume_names = []

        for i in range(self.no_of_output):
            if i >= len(scores):
                break
            ranked_resume_names.append(self.user_accessible_resume[scores[i][0]])

        return ranked_resume_names

    def get_ranking_with_resume_filename(self, path, file_name):

        if path is None or file_name is None:
            return None
        else:
            return None

        scores = self.model_scores.single_resume_scores(path, file_name, self.model)
        ranked_resume_names = []

        for i in range(self.no_of_output):
            if i >= len(scores):
                break
            ranked_resume_names.append(self.user_accessible_resume[scores[i][0]])

        return ranked_resume_names
