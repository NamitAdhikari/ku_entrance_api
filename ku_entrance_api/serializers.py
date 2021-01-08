from rest_framework import serializers

from . import models


class QuestionSerializer (serializers.ModelSerializer):

    class Meta:
        model = models.Questions
        exclude = ['answer']


class QuizSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Quiz
        fields = ['id', 'user', 'quiz_name', 'score']


class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.QstnSubject
        fields = ['subject_name',]


