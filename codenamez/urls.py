from django.contrib import admin
from django.conf.urls import url
from codenamez import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #
    # Auth
    url(r'^register/$', views.user_register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    #
    # Game:
    url(r'^creategame/$', views.create_game, name='create_game'),
    url(r'^joingame/$', views.join_game, name='join_game'),
    url(r'^connectgame/$', views.connect_game, name='connect_game'),
    url(r'^switchteam/$', views.switch_team, name='switch_team'),
    url(r'^startgame/$', views.start_game, name='start_game'),
    url(r'^cancelgame/$', views.cancel_game, name='cancel_game'),
    url(r'^lockturn/$', views.lock_turn, name='lock_turn'),
    url(r'^game/(?P<game_id>[\w\-]+)/$', views.show_game, name='show_game'),
    url(r'^leavegame/(?P<game_id>[\w\-]+)/$', views.leave_game, name='leave_game'),
    #
    # Other:
    url(r'^profile/(?P<profile_id>[\w\-]+)/$', views.show_profile, name='show_profile'),    
    url(r'^howtoplay/$', views.how_to_play, name='how_to_play'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contactus/$', views.contact_us, name='contact_us'),
    url(r'^faq/$', views.faq, name='faq'),
    #url(r'^add_category/$', views.add_category, name='add_category'),
    #url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name='show_category'),
    #url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    #url(r'^register/$', views.register, name='register'),
    #url(r'^login/$', views.user_login, name='login'),
    #url(r'^logout/$', views.user_logout, name='logout'),
    #url(r'^restricted/', views.restricted, name='restricted'),
]
