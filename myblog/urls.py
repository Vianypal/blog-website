from django.urls import path
from . import views

urlpatterns = [
    path('',views.MainView.as_view(),name='index'),
    path('<slug:url_str>',views.PostDetailView.as_view(),name="post-detail"),
    path('login/',views.login_view,name='login'),
    path('signup/',views.signup_view,name="signup"),
    path('logout/',views.logout_view,name='logout'),
    path("contact/",views.ContactView.as_view(),name='contact'),
    path("success/",views.success_view,name="success"),
    path("search/",views.SearchResultsView.as_view(),name='search'),
    path("tag/<slug:slug>",views.TagView.as_view(),name="tag_view"),
    path("<slug:slug>/comments/<int:id>/delete/",views.delete_comment,name="delete_comment"),
]