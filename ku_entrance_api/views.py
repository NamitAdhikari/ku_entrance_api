from django.shortcuts import render
from django.forms.models import model_to_dict

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

import random
import json

from . import serializers
from . import models
from . import permissions

def _generate_code():
    combination = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    return "".join([random.choice(combination) for i in range(40)])


# Create your views here

class PaymentVerify(APIView):

    permission_classes = [IsAuthenticated,]

    def post(self, request, *args, **kwargs):

        user = request.user.username
        code = _generate_code()

        payment = models.PayVerificationCode(user=user, code=code)
        payment.save()

        return Response({
            'status': True,
            'data': 'Payment Successful'
        })



class StartQuiz(APIView):

    permission_classes = [IsAuthenticated,]

    def post(self, request, *args, **kwargs):

        user = request.user
        code = request.POST['code']

        pay_code = models.PayVerificationCode.objects.get(user=user.username)

        if code == pay_code.code:

            getquiz = models.Quiz.objects.get(user=user)

            if getquiz is None:

                quiz = models.Quiz(user=user, quiz_name=f'{user.username}_quiz', activation_code=pay_code)
                quiz.save()

                pay_code.is_active = True
                pay_code.save()

                return Response({
                    'status': True,
                    'data': 'Quiz created successfully'
                })
            else:
                return Response({
                    'status': 'False',
                    'data': 'You already have an existing quiz'
                })

        else:
            return Response({
                'status': False,
                'data': 'Payment Verification Failed'
            })


class Subject(APIView):

    permission_classes = [IsAuthenticated,]   

    def get(self, request, format=None):

        subjects = models.QstnSubject.objects.all()

        serialized_data = serializers.SubjectSerializer(subjects, many=True)
        print(serialized_data)

        return Response({
            'status': True,
            'data': serialized_data.data
        })
    
    def post(self, request, *args, **kwargs):

        # change subject

        user = request.user
        subject_id = request.POST['subjectID']
        quiz_id = request.POST['quizID']

        quiz = models.Quiz.objects.get(id=quiz_id)

        questions = models.Questions.objects.filter(subject=subject_id).order_by('?').first()

        serializer_data = serializers.QuestionSerializer(questions)

        return Response({
            'status': True,
            'data': serializer_data.data
        })


class FetchNextQuestion(APIView):

    permission_classes = [IsAuthenticated,]


    def post(self, request, *args, **kwargs):

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

