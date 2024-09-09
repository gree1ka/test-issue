from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import RequestLog

from testissue.video_logic.video_generator import generate_scrolling_text

import os

def index(request):
    return HttpResponse("hello world!")

def add_db_log(request_type: str = 'Unknown', text: str = 'Unknown'):
    RequestLog.objects.create(
        request_type=request_type,
        text=text
    )

@csrf_exempt
def get_video(request):
    if request.method == 'POST':
        text = request.POST.get('text', 'Ошибка чтения')
    elif request.method == 'GET':
        text = request.GET.get('text', 'Ошибка чтения')
    else:
        add_db_log()
        return HttpResponse('Wrong request type')
    
    if not text:
        add_db_log(request_type=request.method)
        return HttpResponse('text field is empty...')
    
    add_db_log(request_type=request.method, text=text)
    
    generate_scrolling_text(text)

    video_dir = os.path.dirname(os.path.abspath(__file__))
    video_dir = os.path.join(video_dir, '..')
    video_path = os.path.join(video_dir, 'scrolling_text.mp4')

    try:
        video_data = open(video_path, 'rb')
    except Exception as e:
        print(e)
        return  HttpResponse('Error')
    
    response = HttpResponse(video_data, content_type='video/mp4')
    response['Content-Disposition'] = 'attachment; filename="scrolling_text.mp4"'
    return response
