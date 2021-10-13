from django.shortcuts import render

from marketing.models import Signup

from .models import Post

def index(request):
    featured_posts = Post.objects.filter(featured=True)
    latest_posts = Post.objects.order_by('-timestamp')[:3]

    if request.method == 'POST':
        email = request.POST['email']
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    context = {
        'posts_list': featured_posts,
        'latest_posts': latest_posts
    }

    return render(request, 'index.html', context)

def blog(request):
    context = {}
    return render(request, 'blog.html', context)

def post(request):
    context = {}
    return render(request, 'post.html', context)