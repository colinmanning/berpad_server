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

from .models import Person, Role
from .models import Event, Club, Venue
from .models import Sport, SportFacility, SportClub, SportVenue

from .serializers import PersonSerializer, RoleSerializer
from .serializers import UserSerializer
from .serializers import PasswordSerializer
from .serializers import SportSerializer, SportClubSerializer
from .serializers import ClubSerializer
from .serializers import EventSerializer

from django.conf import settings

@api_view(['GET', 'POST'])
def not_allowed(request):
    return Response(status=status.HTTP_404_NOT_FOUND)

'''
A ViewSet to handle roles
'''
class RoleViewSet(viewsets.ModelViewSet):
    """
    The Role class represent categories of users, and can be used to identify which aspects of the system a user can access.
    A role object can have many person objects
    """

    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @detail_route(methods=['get'])
    def people(self, request, pk=None):
        role = self.get_object()
        persons = role.people.all()
        serializer = PersonSerializer(persons, many=True)

        return Response(serializer.data)


'''
A ViewSet to handle persons
'''
class PersonViewSet(viewsets.ModelViewSet):
    """
    The Person class represents someone who can interact with the system. While a User manages things like authentication.
    A Person maintains links to other classes, such as Roles and Businesses.
    A person object has a one to one relationship with a User object.
    A person object can have many roles.

    """
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    """ username is used as the primary key, and must match the username in the linked User object """
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ['username']


    @list_route()
    def all(self, request):
        '''
        Ger all Person objects, with no need to deal with related User objects
        :param request:
        :return:
        '''
        try:
            serializer = PersonSerializer(Person.objects.all(), many=True)
            return Response(serializer.data)
        except:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @list_route()
    def for_role(self, request):
        '''
        Ger all Person objects for a role
        :param request:
        :return:
        '''
        try:
            role_name = request.query_params['name']
            role = Role.objects.get(name=role_name)
            role_persons = []
            for person in role.people.all():
                role_persons.append(person)

            serializer = PersonSerializer(role_persons, many=True)
            return Response(serializer.data)
        except:
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['post'])
    def create_person(self, request):
        '''
        Create a person and user in one call
        '''
        response_message = ''
        response_status = status.HTTP_200_OK
        response_data = {}
        try:
            person = request.data
            person_found = Person.objects.get(username=person['username'])
            response_status = status.HTTP_400_BAD_REQUEST
            response_message = 'Person with username: %s already exists' % (person['username'],)
            r = {'status': response_status, 'message': response_message, 'data': response_data}
            return Response(r)
        except Person.DoesNotExist:
            user_done = False

        try:
            user = User.objects.create_user(person['username'],
                                        person['email'],
                                        person['password'])
            user.first_name = person['first_name']
            user.last_name = person['last_name']

            user.save()
            user.refresh_from_db()
            user_done = True
        except IntegrityError:
            response_status = status.HTTP_400_BAD_REQUEST
            response_message = 'User: %s already exists' % (person['username'],)

        if user_done:
            try:
                new_person = Person.objects.create(username=person['username'])
                new_person.first_name = person['first_name']
                new_person.last_name = person['last_name']
                new_person.save()
                new_person.refresh_from_db()
                for role in person['role']:
                    new_person.role.add(Role.objects.get(pk=role))
                new_person.user = user
                new_person.save()
                response_data = PersonSerializer(new_person).data
                response_message = 'User: %s successfully created' % (person['username'])
            except:
                traceback.print_exc()

                # delete the user
                user.delete()
                try:
                    new_person.delete()
                except:
                    pass
                response_status = status.HTTP_400_BAD_REQUEST
                response_message = 'Error creating user: %s' % (person['username'])

        r = {'status': response_status, 'message': response_message, 'data': response_data}
        return Response(r)

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
    An event takes place over a time period at a Venue
    '''
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

'''
A ViewSet to handle Sports
'''

class SportViewSet(viewsets.ModelViewSet):
    '''
    A Sport can take place at sport venues, managed by sport clubs
    '''
    queryset = Sport.objects.all()
    serializer_class = SportSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

'''
A ViewSet to handle Sport Clubs
'''

class SportClubViewSet(viewsets.ModelViewSet):
    '''
    A Sport Club manages one or more sporting avivities for members
    '''
    queryset = SportClub.objects.all()
    serializer_class = SportClubSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
