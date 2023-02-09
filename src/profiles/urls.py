from django.urls import path
from rest_framework.routers import DefaultRouter

from src.profiles import views


urlpatterns = [
    path('users/', views.UsersView.as_view({"get": "list"}), name='profile'),
    path('users/<int:pk>/', views.UsersView.as_view({"get": "retrieve"}),
         name='detail_profile'),
    path('users/<int:pk>/additionally/', views.AdditionallyProfileView.as_view({"get": "list"}), name='additionally'),
    path('user_me/', views.UserMeView.as_view(
        {"get": "list", "put": "update", "delete": "destroy"}), name='user_me'),
    path('user_me/avatar/', views.AvatarProfileView.as_view(
        {"get": "list", "put": "update"}
        ), name='profile_avatar'),
    path('user_me/social/', views.SocialProfileView.as_view(
        {"get": "list", "post": "create"}
        ), name='social_profile'),
    path('user_me/social/<int:social_pk>/', views.SocialProfileView.as_view(
        {"get": "retrieve", "put": "update", "delete": "destroy"}
        ), name='social_profile_detail'),
    path('title/', views.title, name='title'),
    path('add_git_hub/', views.AddGitHub.as_view(), name='add_git_hub'),
    path('git_hub_auth/', views.GitGubAuthView.as_view(), name='git_hub_auth'),
    path('application/', views.ApplicationView.as_view({'get': 'list', 'post': 'create'})),
    path('application/<int:pk>/', views.ApplicationView.as_view({'delete': 'destroy'})),
    path('application/to_me', views.ApplicationUserGetterView.as_view({'get': 'list'})),
    path('application/to_me/<int:pk>/', views.ApplicationUserGetterView.as_view({'get': 'retrieve'})),
    path('friend/', views.FriendView.as_view({'get': 'list', 'post': 'create'})),
    path('friend/<int:pk>/', views.FriendView.as_view({'delete': 'destroy'})),
    path('social/', views.SocialView.as_view(), name='social'),
    path('languages/', views.LanguageListView.as_view(), name='languages')
]

router = DefaultRouter()
# router.register(r'social', views.SocialView, basename='social')
urlpatterns += router.urls
