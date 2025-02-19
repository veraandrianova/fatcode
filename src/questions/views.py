from django.db.models import Prefetch
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny

from .permissions import IsNotFollower
from ..base.permissions import IsAuthor
from ..base.classes import MixedPermissionSerializer, MixedPermission
from .models import Question, Answer, QuestionReview, AnswerReview, QuestionFollowers
from . import serializers


class QuestionView(MixedPermissionSerializer, ModelViewSet):
    """CRUD вопроса"""
    serializer_classes_by_action = {
        "list": serializers.ListQuestionSerializer,
        "retrieve": serializers.RetrieveQuestionSerializer,
        "update": serializers.UpdateQuestionSerializer,
        "partial_update": serializers.UpdateQuestionSerializer,
        "destroy": serializers.RetrieveQuestionSerializer,
        "create": serializers.CreateQuestionSerializer,
    }
    permission_classes_by_action = {
        "create": (IsAuthenticated,),
        "list": (AllowAny,),
        "update": (IsAuthor,),
        "retrieve": (AllowAny,),
        "partial_update": (IsAuthor,),
        "destroy": (IsAuthor,),
    }

    def get_queryset(self):
        answers = Answer.objects.select_related('author')
        queryset = Question.objects.select_related('author').prefetch_related(
            Prefetch('answers', queryset=answers),
            'tags'
        ).all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AnswerView(MixedPermissionSerializer, ModelViewSet):
    """CRUD ответа"""
    queryset = Answer.objects.all()
    permission_classes = (IsAuthor,)
    permission_classes_by_action = {
        "create": (IsAuthenticated,)
    }
    serializer_classes_by_action = {
        "create": serializers.CreateAnswerSerializer,
        "retrieve": serializers.RetrieveAnswerSerializer,
        "update": serializers.UpdateAnswerSerializer,
        "destroy": serializers.CreateAnswerSerializer,
        "partial_update": serializers.UpdateAnswerSerializer,
    }

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CreateQuestionReview(ModelViewSet):
    """Создать вопрос"""
    serializer_class = serializers.QuestionReviewSerializer
    permission_classes = (IsAuthenticated,)
    queryset = QuestionReview.objects.all()


class CreateAnswerReview(ModelViewSet):
    """Создать ответ"""
    serializer_class = serializers.AnswerReviewSerializer
    permission_classes = (IsAuthenticated,)
    queryset = AnswerReview.objects.all()


class UpdateAnswerAccept(ModelViewSet):
    """Обновить ответ"""
    serializer_class = serializers.UpdateAcceptAnswerSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Answer.objects.select_related('author', 'question', 'parent').all()


class QuestionFollower(MixedPermission, ModelViewSet):
    """Представление подписчиков на вопрос"""
    serializer_class = serializers.FollowerQuestionSerializer
    permission_classes = (IsAuthenticated,)
    permission_classes_by_action = {
        "create": (IsNotFollower, ),
    }

    def get_queryset(self):
        return QuestionFollowers.objects.filter(follower=self.request.user)

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)
