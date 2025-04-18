from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',view=views.home ,name='home'),
    path('posts/',view=views.posts,name='posts'),
    path('add_post/',view=views.addPost,name='add-admin'),
    path('post_details/<int:id>',view=views.PostDetails,name='post-details'),
    path('register/',view=views.register,name='register'),
    path('login/',view=views.login,name='login'),
    path('logout/',view=views.logout,name='logout'),

    path('protected_view/',view=views.protected_view,name='protected_view'),

]