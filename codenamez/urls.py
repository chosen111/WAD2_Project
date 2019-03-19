from django.contrib import admin
from django.conf.urls import url
from codenamez import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.user_register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^creategame/$', views.game_create, name='create_game'),
    url(r'^joingame/$', views.game_join, name='join_game'),
    url(r'^profile/(?P<profile_id>[\w\-]+)/$', views.show_profile, name='show_profile'),
    url(r'^game/(?P<game_id>[\w\-]+)/$', views.show_game, name='show_game'),
    url(r'^leavegame/(?P<game_id>[\w\-]+)/$', views.leave_game, name='leave_game'),

    #url(r'^about/', views.about, name='about'),
    #url(r'^add_category/$', views.add_category, name='add_category'),
    #url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name='show_category'),
    #url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    #url(r'^register/$', views.register, name='register'),
    #url(r'^login/$', views.user_login, name='login'),
    #url(r'^logout/$', views.user_logout, name='logout'),
    #url(r'^restricted/', views.restricted, name='restricted'),
]
