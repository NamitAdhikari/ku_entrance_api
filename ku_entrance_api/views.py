from django.shortcuts import render
from django.forms.models import model_to_dict

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser


from . import serializers
from . import models
from . import permissions

# Create your views here.

class UserProfileView(viewsets.ModelViewSet):

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    
    permission_classes = [IsAdminUser,]

    authentication_classes = [TokenAuthentication, ]


class SubjectView(viewsets.ModelViewSet):

    serializer_class = serializers.SubjectSerializer
    queryset = models.QstnSubject.objects.all()

    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]
    
    allowed_methods = ['GET', 'POST',]

    def create(self, request):
        if request.user.is_superuser:

            serializer = serializers.SubjectSerializer(data=request.data)

            if serializer.is_valid():
                subject = models.QstnSubject(
                    subject_name = serializer.data.get('subject_name'),
                    totQuestions = serializer.data.get('totQuestions')
                )
                subject.save()

                return Response({
                    "subject_name": serializer.data.get('subject_name'),
                    "totQuestions": serializer.data.get('totQuestions')
                })

        else:
            return Response({"Need to be admin to perform this task"})



class QuestionView(viewsets.ModelViewSet):

    serializer_class = serializers.QuestionSerializer
    queryset = models.Questions.objects.all()



class FetchNextQuestion(APIView):

    permission_classes = [IsAuthenticated,]


    def post(self, request, *args, **kwargs):

        print(request.data)

        quiz_id = request.POST['quizID']
        answer = request.POST['answer']

        question_id = request.POST['questionID']

        quiz = models.Quiz.objects.get(id=quiz_id)

        try:

            if request.user == quiz.user:

                next_question = models.Questions.objects.fetch_next(question_id, answer, quiz_id)

                if next_question is None:
                    raise ValueError('Subject Completed')

                elif next_question == -1:
                    return Response({
                        'status': False,
                        'data': 'You have already attempted this question'
                    })

                print(f"next question = {next_question}")

                serialized_data = serializers.QuestionSerializer(next_question)

                return Response({
                    'status': True,
                    'data': serialized_data.data
                })

            else:
                return Response({
                    'status': False,
                    'data': "You don't have permission to attend this quiz"
                })

        except ValueError:
            return Response({
                'status': False,
                'data': 'You have completed this subject'
            })




    