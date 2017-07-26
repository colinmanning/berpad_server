import datetime
import json
import traceback
import ephem
import re
import mimetypes
import os
import requests
import pytz
import csv
import io
import math
import boto3
import sys

import subprocess
from subprocess import CalledProcessError

from .range_streaming import RangeFileWrapper

from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.decorators import api_view, detail_route, list_route
from rest_framework.response import Response
from django.http import StreamingHttpResponse
from django.http import FileResponse
from wsgiref.util import FileWrapper

from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.decorators import api_view, detail_route, list_route
from rest_framework.response import Response
from django.http import StreamingHttpResponse
from django.http import FileResponse
from wsgiref.util import FileWrapper

from django.db.utils import IntegrityError

from .models import Event

from .serializers import EventSerializer

from django.conf import settings

@api_view(['GET', 'POST'])
def not_allowed(request):
    return Response(status=status.HTTP_404_NOT_FOUND)
class UserViewSet(viewsets.ModelViewSet):
    """
    The User class represents an authenticatable user in the system.
    A user object will typically have a one to one relationship with a person object
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @detail_route(methods=['post'])
    def set_password(self, request, pk=None):
        """
        Set a users password via thew api
        :param request:
        :param pk:
        :return:
        """

        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @list_route()
    def recent_users(self, request):
        recent_users = User.objects.all().order('-last_login')

        serializer = self.get_serializer(recent_users, many=True)
        return Response(serializer.data)

'''
A ViewSet to handle Events
'''

class EventViewSet(viewsets.ModelViewSet):
    '''
    A Program for which proposals are made
    '''
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
