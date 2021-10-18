from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q
from django.shortcuts import render

from marketing.models import Signup

from .models import Post


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
        'latest_posts': most_recent,
        'category_count': category_count
    }

    return render(request, 'blog.html', context)

def post(request, pk):
    context = {}
    return render(request, 'post.html', context)