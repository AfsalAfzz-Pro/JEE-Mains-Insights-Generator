from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
import urllib.parse
from django.template.loader import render_to_string

import google.generativeai as genai
import markdown
from .Data_Processing import file_hunt, ai_response, stream_chat
# Create your views here.
last_appended = []

def entrance(request):
    return render(request, 'Entrance.html')


def this_year_paper(request):
    return render(request, 'Insights.html')


def select_papers(request):
    file_names= file_hunt()
    files = []
    for file in file_names:
        files.append(file[29:44])
    dict1 = {'files':files}
    # print(dict1)
    return render(request, 'Paper_Selection.html', context=dict1)

def pdf_data(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        print(message)
        filenames = file_hunt()
        for file in filenames:
            if message in file:
                target = file
                break
        ai_resp = markdown.markdown(ai_response(path=target))
        last_appended.append(ai_resp)
        html = render_to_string('chatbot.html', {'data':ai_resp, 'filename':message})
        return JsonResponse(request, html, safe=False)
    

def chatbot(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        print('prompt recieved')
        print(prompt)
        # response_data = {'response':'yes sure why not'}
        response_data = markdown.markdown(stream_chat(prompt))
        # html = render_to_string('chatbot.html', {'response':'yes sure why not'})
        return JsonResponse(request, response_data, safe=False)








