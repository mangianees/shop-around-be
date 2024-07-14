from django.http import JsonResponse

def error_400(request, exception):
    message = 'Invalid data request'

    response = JsonResponse(data={'message' : message, 'status_code' : 400})
    response.status_code = 400
    return response

def error_404(request, exception):
    message = 'Your URL is bad and you should feel bad'

    response = JsonResponse(data={'message' : message, 'status_code' : 404})
    response.status_code = 404
    return response

def error_500(request):
    message = 'An internal server error has occurred'

    response = JsonResponse(data={'message' : message, 'status_code' : 500})
    response.status_code = 500
    return response