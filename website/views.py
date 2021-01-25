import pickle

from django.shortcuts import render

from Production.RankResult import RankResult


def search_result(no_of_output, query_option, direct, resume_id, upload):
    if no_of_output is None:
        no_of_output = 1
    if resume_id is None:
        resume_id = 1
    ranked_result = RankResult(int(no_of_output), 'BM25Okapi')

    with open('Data/Workin_Data/' + 'data_dict.pkl', 'rb') as f:
        pickle_data = pickle.load(f)
    resume_count = pickle_data['resume_count']

    options = {
        "direct_search": ranked_result.get_ranking_with_query(direct),
        "resume_id": ranked_result.get_ranking_with_resume_id(int(resume_id)),
        "file_upload": ranked_result.get_ranking_with_resume_filename(upload)
    }
    return resume_count, options.get(query_option)


def home(request):
    resume_id = request.GET.get('id')
    upload = request.GET.get('upload')
    direct = request.GET.get('direct')
    no_of_outputs = request.GET.get('no_of_outputs')
    query_option = request.GET.get('query_option')

    result = search_result(no_of_outputs, query_option, direct, resume_id, upload)

    return render(request, 'website/resume_rank.html', {'result': result[1], 'no_of_resumes': result[0]})
