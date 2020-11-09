from datetime import datetime, timedelta
from uuid import uuid4
from django.contrib.auth.models import User
from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, ProfileSerializer, ProfileListSerializer, SubscribeSerializer
from .models import Profile, Subscribe


class ProfileDetail(APIView):

    @staticmethod
    def get_object_by_pk(profile_id):
        try:
            return Profile.objects.get(pk=profile_id)
        except Profile.DoesNotExist:
            raise exceptions.ValidationError({"profile_id": ["Profile not found"]})

    @staticmethod
    def get_object_by_token(token):
        try:
            return Profile.objects.get(token=token)
        except Profile.DoesNotExist:
            raise exceptions.AuthenticationFailed({"token": ["Token is invalid"]})

    def get(self, request, profile_id):
        pk = profile_id
        profile = self.get_object_by_pk(pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serialized = UserSerializer(data=request.data)
        if serialized.is_valid():
            user = User()
            user.username = serialized.data['username']
            user.set_password(serialized.data['password'])
            user.token = uuid4()
            user.save()
            profile = user.profile
            profile.subscribe = SubscribeDetail.create_subscribe(profile.id, duration=14)
            serializer = ProfileSerializer(profile)
            return Response({**serializer.data, 'token': user.token}, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileList(APIView):

    def get(self, request):
        books = Profile.objects.all()
        serializer = ProfileListSerializer(books, many=True)
        return Response(serializer.data)


class SubscribeDetail(APIView):

    @staticmethod
    def create_subscribe(profile_id, duration):
        subscribe = Subscribe()
        subscribe.finish = datetime.now().date() + timedelta(days=duration)
        subscribe.related_profile = profile_id   # extra field for post_save signal
        subscribe.save()
        return subscribe

    @staticmethod
    def check_subscribe(profile_id=None, token=None):

        # if profile_id and token will be realized if need
        if profile_id:
            profile = ProfileDetail.get_object_by_pk(profile_id)
        elif token:
            profile = ProfileDetail.get_object_by_token(token)
        else:
            profile = None

        if profile and profile.subscribe and (profile.subscribe.finish > datetime.now().date()):
            return True


    def post(self, request):
        serialized = SubscribeSerializer(data=request.data, context={'request': request})
        if serialized.is_valid():
            duration = int(request.data['duration'])
            profile_id = int(request.data['profile_id'])

            if SubscribeDetail.check_subscribe(profile_id=profile_id):
                raise exceptions.ValidationError({"profile_id": ["profile still have actual subscription"]})

            subscribe = self.create_subscribe(profile_id, duration)

            serializer = SubscribeSerializer(subscribe)
            additional = {'profile_id': profile_id}
            return Response({**serializer.data, **additional}, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)
