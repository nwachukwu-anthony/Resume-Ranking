import pickle

from django.shortcuts import render

from Production.RankResult import RankResult


def search_result(no_of_output, resume_words_counts, query_option, direct, resume_id, model):
    if no_of_output is None:
        no_of_output = 1
    if resume_words_counts is None:
        resume_words_counts = 100
    if resume_id is None:
        resume_id = 1
    ranked_result = RankResult(int(no_of_output), int(resume_words_counts), model)

    with open('Data/Workin_Data/' + 'data_dict.pkl', 'rb') as f:
        pickle_data = pickle.load(f)
    resume_count = pickle_data['resume_count']

    options = {
        "direct_search": ranked_result.get_ranking_with_query(direct),
        "resume_id": ranked_result.get_ranking_with_resume_id(int(resume_id)),
    }
    return resume_count, options.get(query_option)


def home(request):
    resume_id = request.GET.get('id')
    direct = request.GET.get('direct')
    no_of_outputs = request.GET.get('no_of_outputs')
    resume_words_counts = request.GET.get('resume_words_counts')
    query_option = request.GET.get('query_option')
    model = request.GET.get('model')

    result = search_result(no_of_outputs, resume_words_counts, query_option, direct, resume_id, model)

    return render(request, 'website/resume_rank.html', {'result': result[1], 'no_of_resumes': result[0]})
