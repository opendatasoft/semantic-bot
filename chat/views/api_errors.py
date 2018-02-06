from django.http.response import HttpResponse


def bad_format_correspondance():
    response = HttpResponse(
        "Request format is not valid",
        content_type='application/json',
        status=400)
    response['Access-Control-Allow-Origin'] = '*'
    return response
