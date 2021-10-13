from django.shortcuts import render

def index(request):
    context = {}
    return render(request, 'index.html', context)

def blog(request):
    context = {}
    return render(request, 'blog.html', context)