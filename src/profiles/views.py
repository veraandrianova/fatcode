from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework import permissions, parsers
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filter

from src.profiles import models, serializers, services, filters
from src.base.classes import MixedPermissionSerializer
from src.base.permissions import IsUser
from .permissions import IsQuestionnaireNotExists
from src.team.models import Team


def title(request):
    """Для добавления git только авторизованным"""
    if request.user.is_authenticated:
        return render(request, 'profiles/title.html')
    else:
        return render(request, 'profiles/title_auth.html')


class GitGubAuthView(generics.GenericAPIView):
    """Авторизация через Гитхаб"""
    serializer_class = serializers.GitHubAddSerializer

    def post(self, request):
        ser = serializers.GitHubAddSerializer(data=request.data)
        if ser.is_valid():
            account_name, account_url, account_id, email = services.github_get_user_auth(ser.data.get("code"))
            if internal_token := services.check_account_for_auth(account_id):
                return Response(status.HTTP_200_OK)
            else:
                internal_token = services.create_user_and_token(account_id, email, account_name, account_url)
                return Response(status.HTTP_200_OK)


class AddGitHub(generics.GenericAPIView):
    """Добавление git к существующему пользователю"""
    serializer_class = serializers.GitHubAddSerializer

    def post(self, request):
        ser = serializers.GitHubAddSerializer(data=request.data)
        if ser.is_valid():
            account_name, account_url, account_id = services.github_get_user_add(ser.data.get("code"))
            if services.check_account_for_add(request.user, account_id):
                services.create_account(request.user, account_name, account_url, account_id)
                return Response(status.HTTP_200_OK)


class UserView(ModelViewSet):
    """Internal user display"""

    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return models.FatUser.objects.filter(id=self.request.user.id)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)
        return obj


class UserPublicView(ModelViewSet):
    """Public user display"""

    queryset = models.FatUser.objects.all()
    serializer_class = serializers.UserPublicSerializer
    permission_classes = [permissions.AllowAny]


class SocialView(ReadOnlyModelViewSet):
    """List or one entry social display"""
    queryset = models.Social.objects.all()
    serializer_class = serializers.ListSocialSerializer

    def get_queryset(self):
        return models.Social.objects.all()


class UserAvatar(ModelViewSet):
    """Create and update user avatar"""

    parser_classes = [parsers.MultiPartParser]
    serializer_class = serializers.UserAvatarSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return models.FatUser.objects.filter(id=self.request.user.id)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)
        return obj


class QuestionnaireView(MixedPermissionSerializer, ModelViewSet):
    """CRUD анкеты пользователя"""
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'create': (IsQuestionnaireNotExists,),
        'retrieve': (IsAuthenticated, ),
        'update': (IsUser,),
        'destroy': (IsUser,),
    }
    serializer_classes_by_action = {
        'list': serializers.QuestionnaireListSerializer,
        'retrieve': serializers.QuestionnaireSerializer,
        'create': serializers.QuestionnaireSerializer,
        'update': serializers.QuestionnaireSerializer,
        'destroy': serializers.QuestionnaireSerializer
    }
    filter_backends = (filter.DjangoFilterBackend,)
    filterset_class = filters.ToolkitFilter

    def get_queryset(self):
        # teams = Team.objects.filter(user=self.request.user)
        # print(teams)
        # questionnaire = models.Questionnaire.objects.filter(
        #     teams=Q(teams__user=self.request.user))
        #
        # print(questionnaire)
        # return questionnaire
        return models.Questionnaire.objects.all().prefetch_related('user', 'teams', 'projects', 'accounts', 'category', 'socials')

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
