from django.shortcuts import render, HttpResponse
from home.models import Task
from django.http import JsonResponse

def task_1(request):
    b = Task.custom_object.open_tasks().values_list('status') 
    return JsonResponse({'context': list(b)})