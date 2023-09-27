from django.shortcuts import render
from .models import Question

def math_table(request):
    math_list = Question.objects.all()
    return render(request, 'index.html', {'math_list': math_list})