from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "status": "success",
        "message": "Welcome to GhostAI - AI Assistant API",
        "app": "ghostai"
    })
