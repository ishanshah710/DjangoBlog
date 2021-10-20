from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render, reverse

from marketing.models import Signup
from posts.forms import CommentForm, PostForm

from .models import Author, Post


def get_author(user):
    qs = Author.objects.filter(user=user)

    if qs.exists():
        return qs[0]

    return None

def search_results(request):
    query = request.GET.get('q')

    queryset = Post.objects.all()

    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()

    context = {
        'queryset': queryset,
        'query': query
    }

    return render(request, 'search_results.html', context)

def get_category_count():
    queryset = Post \
        .objects \
        .values('categories__title') \
        .annotate(Count('categories__title'))

    # cats = Post.objects.filter('categories__title')

    # for ct in cats:
    #     print(ct)

    return queryset

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
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post_list = Post.objects.all()
    
    category_count = get_category_count()
    
    # 2nd arg is posts per page that we want to keep
    paginator = Paginator(post_list, 2)

    page_request_variable = 'page'

    # this 'page' (type : int) parameter can be passed in url to render to that page directly if valid
    page = request.GET.get(page_request_variable)

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        # if page is not int and of invalid type then we will show 1st page
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        # if page is empty then we will show last page
        paginated_queryset = paginator.page(paginator.num_pages)
    
    context = {
        # 'post_list': post_list,
        'page_request_var': page_request_variable,
        'paginated_queryset': paginated_queryset,
        'most_recent': most_recent,
        'category_count': category_count
    }

    return render(request, 'blog.html', context)

def post(request, pk):

    post = get_object_or_404(Post, pk=pk)
    most_recent = Post.objects.order_by('-timestamp')[:3]
    category_count = get_category_count()

    form = CommentForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'pk': post.pk,
            }))

    context = {
        'post': post,
        'most_recent': most_recent,
        'category_count': category_count,
        'form':form
    }
    return render(request, 'post.html', context)

def post_create(request):
    title = 'Create'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)

    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse('post-detail', kwargs={
                'pk': form.instance.pk
            }))

    context = {
        'form': form,
        'title': title
    }
    return render(request, "post_create.html", context)

def post_update(request, pk):
    title = 'Update'
    post = get_object_or_404(Post, pk=pk)
    
    form = PostForm(
        request.POST or None, 
        request.FILES or None, 
        instance=post)
    author = get_author(request.user)

    if request.method == 'POST':
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse('post-detail', kwargs={
                'pk': form.instance.pk
            }))

    context = {
        'form': form,
        'title': title
    }
    return render(request, "post_create.html", context)

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect(reverse('post-list'))

