from rest_framework import serializers

from . import models


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UserProfile
        fields = ('id', 'username', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        user = models.UserProfile(
            username = validated_data['username'],
            name = validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user



class SubjectSerializer (serializers.ModelSerializer):

    class Meta:
        model = models.QstnSubject
        fields = '__all__'



class QuestionSerializer (serializers.ModelSerializer):

    class Meta:
        model = models.Questions
        exclude = ['answer']









# class initQuizSerializer (serializers.ModelSerializer):

#     class Meta:
#         model = models.Quiz
#         fields = ('subject')