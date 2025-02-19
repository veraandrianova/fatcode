from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

teams = views.TeamView.as_view({
    'get': 'list',
    'post': 'create'
})

detail_teams = views.TeamView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

my_team = views.OwnTeamListView.as_view({
    'get': 'list',
})

team_member = views.MemberTeamListView.as_view({
    'get': 'list'
})


post = views.PostView.as_view({
    'get': 'list',
    'post': 'create'
})

update_or_delete_post = views.PostView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})
comment = views.CommentsView.as_view({
    'get': 'list',
    'post': 'create'
})

comment_detail = views.CommentsView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

invitation = views.InvitationView.as_view({
    'get': 'list',
    'post': 'create'
})

invitation_delete = views.InvitationView.as_view({
    'get': 'retrieve',
    'delete': 'destroy'
})

invitation_list = views.InvitationDetailView.as_view({
    'get': 'list'
})

invitation_detail = views.InvitationDetailView.as_view({
    'get': 'retrieve',
    'put': 'update'
})

social_links = views.SocialLinkView.as_view({
    'get': 'list',
    'post': 'create'
})

social_link_detail = views.SocialLinkView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

member = views.MemberList.as_view({
    'get': 'list',
})

member_detail = views.MemberList.as_view({
    'get': 'retrieve',
    'delete': 'destroy'
})

avatar_team = views.AvatarTeam.as_view({
    'get': 'list',
    'put': 'update'
})

urlpatterns = ([
    path('my_team/', my_team, name='my_team'),
    path('team_member/', team_member, name='team_member'),
    path('invitation/', invitation, name='invitation'),
    path('invitation/<int:pk>/', invitation_delete, name='invitation_delete'),
    path('invitation_list/', invitation_list, name='invitation_list'),
    path('invitation_list/<int:pk>/', invitation_detail, name='invitation_detail'),
    path('<int:pk>/social_link/', social_links, name='social_links'),
    path('<int:pk>/social_link/<int:social_pk>/', social_link_detail, name='social_link_detail'),
    path('<int:pk>/member/', member, name='member'),
    path('<int:pk>/member/<int:member_pk>/', member_detail, name='member_detail'),
    path('<int:pk>/post/', post, name='post'),
    path('<int:pk>/post/<int:post_pk>/', update_or_delete_post, name='update_or_delete_post'),
    path('<int:pk>/post/<int:post_pk>/comment/', comment, name='comment'),
    path('<int:pk>/post/<int:post_pk>/comment/<int:comment_pk>', comment_detail, name='comment_detail'),
    path('<int:pk>/avatar/', avatar_team, name='avatar_team'),
    path('<int:pk>/', detail_teams, name='detail_teams'),
    path('', teams, name='teams'),
])
