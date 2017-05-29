from django.conf.urls import url
from todos import views, views_api

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^create/$', views.create, name = "create"),
    url(r'^contact$', views.contact, name= "contact"),
    url(r'^about$', views.about, name= "about"),
    url(r'^save$', views.save, name= "save"),
    url(r'^edit/todos/(\d+)/$', views.edit, name= "edit"),
    url(r'^remove/(\d+)/$', views.remove, name= "remove"),
    # API Route for Ajax
    url(r'^api/todos/(\d+)$', views_api.update, name='api_update_todo'),
    url(r'^login$', views.login, name= "login"),
    url(r'^submit$', views.submit, name= "submit"),
    url(r'^logout$', views.logout, name= "logout"),
    url(r'^signup/$', views.signup, name="signup"),
    url(r'^sign_up/$', views.sign_up, name= "sign_up"),
    #rest api list
    url(r'^api/todos$', views.TodoListView.as_view(), name='api_todo_list'),
    url(r'^api/todos/(?P<pk>[0-9]+)$', views.TodoItemView.as_view(), name='api_todo_item')

    ]
