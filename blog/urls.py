from django.urls import include, path
from . import views

app_name = 'blog'

urlpatterns = [
    path('',views.blog_list, name='list'),
    path('view/<int:pk>', views.blog_view, name ='view'),
    path('user/<str:username>/', views.user_posts, name='user_posts'),
    path('create/', views.create_post, name='create_post'),
    path('update/<int:pk>/', views.update_post, name='update_post'),
    path('delete/<int:pk>/', views.delete_post, name='delete_post'),
    
]