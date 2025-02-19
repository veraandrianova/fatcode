from rest_framework import serializers
from ..profiles.serializers import GetUserSerializer

from . import models
from .services import QuestionService, AnswerService, create_follow
from .validators import QuestionValidator
from ..profiles.services import ReputationService


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ("id", "name")
        read_only_fields = ("id",)


class CreateAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ("text", "parent", "question")


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value)
        return serializer.data


class RetrieveAnswerSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)

    class Meta:
        model = models.Answer
        fields = ("id", "text", "children", "question")


class AnswerSerializer(serializers.ModelSerializer):
    author = GetUserSerializer(required=False)
    children_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Answer
        fields = (
            "author",
            "text",
            "parent",
            "date",
            "updated",
            "rating",
            "accepted",
            "question",
            "children_count",
        )

    def get_children_count(self, instance):
        return instance.children.count()


class CreateQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = ("title", "text")

    def create(self, validated_data):
        question = self.Meta.model.objects.create(**validated_data)
        create_follow(question, validated_data['author'])
        return question


class RetrieveQuestionSerializer(serializers.ModelSerializer):
    author = GetUserSerializer(read_only=True)
    answers = AnswerSerializer(many=True, read_only=True)
    tags = TagsSerializer(many=True, read_only=True)

    class Meta:
        model = models.Question
        fields = (
            "asked",
            "viewed",
            "text",
            "tags",
            "rating",
            "author",
            "updated",
            "answers",
            "title",
        )


class ListQuestionSerializer(serializers.ModelSerializer):
    author = GetUserSerializer()
    correct_answers = serializers.SerializerMethodField()
    answer_count = serializers.SerializerMethodField()
    tags = TagsSerializer(many=True, read_only=True)

    class Meta:
        model = models.Question
        fields = (
            "id",
            "title",
            "rating",
            "author",
            "viewed",
            "correct_answers",
            "answer_count",
            "tags",
        )

    def get_correct_answers(self, instance):
        return QuestionService(instance).correct_answers_count()

    def get_answer_count(self, instance):
        return QuestionService(instance).answers_count()


class QuestionReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuestionReview
        fields = ("grade", "question")

    def validate(self, data):
        data["user"] = self.context["request"].user
        QuestionValidator().check_review(data)
        return data

    def create(self, validated_data):
        review = self.Meta.model.objects.create(**validated_data)
        QuestionService(validated_data["question"]).update_rating(validated_data['grade'])
        return review


class AnswerReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnswerReview
        fields = ("grade", "answer")

    def validate(self, data):
        data["user"] = self.context["request"].user
        QuestionValidator().check_review(data)
        return data

    def create(self, validated_data):
        review = self.Meta.model.objects.create(**validated_data)
        AnswerService(validated_data["answer"]).update_rating(validated_data['grade'])
        return review


class UpdateQuestionSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True, read_only=False)

    class Meta:
        model = models.Question
        fields = ("title", "text", "tags")

    def update(self, instance, validated_data):
        tags_data = validated_data.pop("tags")
        service = QuestionService(instance)
        service.update_tags(tags_data)
        instance = super(UpdateQuestionSerializer, self).update(instance, validated_data)
        return instance


class UpdateAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ("text",)


class UpdateAcceptAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ("accepted",)

    def update(self, instance, validated_data):
        AnswerService(instance).update_accept()
        return super(UpdateAcceptAnswerSerializer, self).update(instance, validated_data)


class FollowerQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuestionFollowers
        fields = ('id', 'question')


