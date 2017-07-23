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

from django.db.utils import IntegrityError

from .models import Event

from .serializers import EventSerializer

from django.conf import settings

@api_view(['GET', 'POST'])
def not_allowed(request):
    return Response(status=status.HTTP_404_NOT_FOUND)

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
