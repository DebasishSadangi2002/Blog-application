from django.http import HttpResponse
from django.shortcuts import render
from blog.models import Post


    

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    latest_post = posts.first() if posts else None
    return render(request, 'home.html', { 'latest_post': latest_post})