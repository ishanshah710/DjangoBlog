from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.deletion import CASCADE
from django.urls import reverse

from tinymce import HTMLField


# Create your models here.

User = get_user_model()

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username
    
    class Meta:
        db_table = 'Author'

class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Category'

class Post(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    content = HTMLField()
    
    comment_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    categories = models.ManyToManyField(Category)

    featured = models.BooleanField()

    previous_post = models.ForeignKey('self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Post'
    
    def get_absolute_url(self, ):
        return reverse('post-detail', kwargs={
            'pk': self.pk
        })
    
    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return '{} - {} : {}'.format(self.pk, self.user.username, self.post.title)