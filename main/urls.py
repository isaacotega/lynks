from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('posts', views.posts, name='posts'),
	path('post', views.post, name='post'),
	path('signup', views.signup, name='signup'),
	path('login', views.login, name='login'),
	path("redirector", views.redirector, name='redirector'),
	path("report", views.report, name='report'),
	path('styles/posts', views.styles.posts, name='styles-posts'),
	path('scripts/posts.js', views.scripts.posts, name='scripts-posts'),
	path('ajax-handlers/posts', views.ajaxHandlers.posts, name='ajax-handlers-posts'),
	path('ajax-handlers/post-actions', views.ajaxHandlers.postActions, name='ajax-handlers-postActions')
]