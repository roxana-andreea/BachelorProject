from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^login/$', views.login_user, name='login_user'),
	url(r'^logout/$', views.logout_user, name='logout_user'),
	url(r'^add_user/$', views.add_user, name='add_user'),
	url(r'^alert_save/$', views.alert_save, name='alert_save'),
    url(r'^$', views.index, name='index'),
]
