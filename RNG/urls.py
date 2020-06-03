from django.conf.urls import url
from RNG import views
from django.conf.urls.static import static
from django.conf import settings

#url patterns linking each page to a url
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^category/$', views.show_categories, name='show_categories'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
	url(r'^category/(?P<category_name_slug>[\w\-]+)/(?P<game_name_slug>[\w\-]+)/$', views.gameV, name='game'),
	
    url(r'^add_game/$', views.add_gameV, name='add_game'),
	
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signin/$', views.user_login, name='signin'),
    url(r'^signout/$', views.user_logout, name='signout'),
    url(r'^search', views.search, name='search'),
    url(r'^allgames', views.allgames, name='allgames')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
