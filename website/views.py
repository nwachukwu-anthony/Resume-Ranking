from django.shortcuts import render

from Production.RankResult import RankResult


def search_result(no_of_output, query_option, direct, resume_id, upload):
    ranked_result = RankResult(no_of_output, 'BM25Okapi')

    options = {
        "direct_search": ranked_result.get_ranking_with_query(direct),
        "resume_id": ranked_result.get_ranking_with_resume_id(resume_id),
        "file_upload": ranked_result.get_ranking_with_resume_filename(path="./../Data/Resumes/", file_name=upload)
    }
    return options.get(query_option)


def home(request):
    resume_id = request.GET.get('id')
    upload = request.GET.get('upload')
    direct = request.GET.get('direct')
    query_option = request.GET.get('query_option')
    no_of_output = request.GET.get('no_of_output')

    result = search_result(no_of_output, query_option, direct, resume_id, upload)

    return render(request, 'website/resume_rank.html', {'result': result})
