from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    
    path('', views.HomePage.as_view(), name="home"),
    path('login', views.LoginPage.as_view(), name="login" ),
    path('signup', views.SignupPage.as_view(), name="signup"),
    path('post',views.PostPage.as_view(),name="post"),
    path('thaithai',views.BlogPage.as_view(),name="blog"),
    path('search',views.SearchPage.as_view(),name="search"),    
    path('logout', views.LogoutPage.as_view(), name="logout"),
    path('profile', views.ProfilePage.as_view(), name="profile"),
    
    # ! all post
    path('post',views.PostPage.as_view(),name="post"),
    path('post/<int:post_id>/', views.post_detail.as_view(), name='post_detail'),
    path('post/<int:post_id>/comments/', views.post_comments.as_view(), name='post_comments'),
    path('post/<int:post_id>/share/', views.Share_post.as_view(), name='share_post'),
    path('delete/<int:post_id>/', views.PostDeleteView.as_view(), name="post_delete"),
]

#! path to call picture
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)