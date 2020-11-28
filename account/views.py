from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from . import models

# Create your views here.

class UserView(APIView):

    def post(self, request, *args, **kwargs):

        username = request.POST['username']
        name = request.POST['name']
        password = request.POST['password']

        user = models.UserProfile(username=username, name=name)
        user.set_password(password)
        user.save()

        return Response({
            'status': 'True',
            'data': {
                'message': 'User Created Successfully',
                'id': user.id,
                'username': user.username,
                'name': user.name
            }
        })