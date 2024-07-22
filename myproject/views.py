from django.http import HttpResponse
from django.shortcuts import render
from blog.models import Post


    

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    latest_post = posts.first() if posts else None
    return render(request, 'home.html', { 'latest_post': latest_post})

from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration.html', {'form':form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data= request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form':form})

def logout_view(request):
    logout(request)
    return redirect('home')

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .forms import CommentForm, PostForm
from django.contrib.auth.models import User
from .models import Post , Comment

# Create your views here.
def blog_list(request):
    blogs = Post.objects.all().order_by('-created_at')
    return render(request, 'list.html', {'blogs':blogs})

def blog_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('view', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'view.html', {'post': post, 'comments': comments, 'form': form})

def user_posts(request, username):
    user = get_object_or_404(User, username=username)
    user_posts = Post.objects.filter(writer=user).order_by('-created_at')
    return render(request, 'user_posts.html', {'user': user, 'user_posts': user_posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.writer = request.user
            post.save()
            return redirect('home')  # Redirect to home or post detail page
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.writer:
        return redirect('home')  # Redirect or handle unauthorized access
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('view', pk=post.pk)  # Redirect to post detail page
    else:
        form = PostForm(instance=post)
    return render(request, 'update_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.writer:
        return redirect('home')  # Redirect or handle unauthorized access
    if request.method == 'POST':
        post.delete()
        return redirect('home')  # Redirect to home or another page after deletion
    return render(request, 'delete_post.html', {'post': post})