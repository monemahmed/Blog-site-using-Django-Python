from .feeds import LatestPostsFeed
from django.urls import path
from. import views


app_name = 'blog'
urlpatterns = [path('', views.post_list, name='post_list'),
               path('tag/<slug:tag_slug>', views.post_list,
                    name='post_list_by_tag_name'),
               path('feed/', LatestPostsFeed(), name='post_feed'),

               path('<slug:post>/', views.post_detail, name='post_detail'),
               path('<int:post_id>/share', views.post_share, name='post_share'), ]
