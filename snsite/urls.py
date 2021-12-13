"""snsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# import debug_toolbar
from re import template
from django.contrib import admin
from django.urls import path, include
from anime.views import (home,CreatePostView, 
                         PostDetailView,ChannelDetailView, comment_submit, 
                         read_all_notification,ChannelAutoCompleteView,
                         SearchChannelView,vote,join_channel,
                         CreateChannelView,HomePage,
                         ChannelUpdateView,PostUpdateView,PostDeleteView,
                         subcomment_submit,
                         badges)
from django.conf.urls.static import static
from snsite import settings
urlpatterns = [
    # path('__debug__/', include(debug_toolbar.urls)),
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('accounts/', include('users.urls')),
    path('',HomePage.as_view(),name='homepage'),
    path('channel/<slug:slug>/post/<int:pk>/',PostDetailView.as_view(), name="post-detail"),
    path('channel/<slug:slug>/post-submit/',CreatePostView.as_view(),name="post-submit"),
    path('channel/<slug:slug>/post/<int:pk>/comment-submit/',comment_submit,name='comment-submit'),
    path('channel/<slug:slug>/',ChannelDetailView.as_view(),name='channel-detail'),
    path('read-all-notification/',read_all_notification,name='read-all-notification'),
    path('channel-autocomplete/',ChannelAutoCompleteView.as_view(),name='channel-autocomplete'),
    path('search/',SearchChannelView.as_view(),name='channel-search'),
    path('vote/',vote,name='vote'),
    path('channel/<slug:slug>/join-channel/',join_channel,name='channel-join'),
    path('create-channel/',CreateChannelView.as_view(),name='channel-create'),
    path('channel/<slug:slug>/update-channel/',ChannelUpdateView.as_view(),name="channel-update"),
    path('channel/<slug:slug>/post/<int:pk>/update/',PostUpdateView.as_view(),name="post-update"),
    path('channel/<slug:slug>/post/<int:pk>/delete/',PostDeleteView.as_view(),name="post-delete"),
    path('create-subcomment/',subcomment_submit,name="create-subcomment"),
    path('badges/',badges,name="badges"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 


