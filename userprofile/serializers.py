from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Subscribe


class SubscribeSerializer(serializers.ModelSerializer):

    finish = serializers.DateField(required=False)

    class Meta:
        model = Subscribe
        fields = ('id', 'start', 'finish')

    def validate(self, obj):

        dur = self.context['request'].data.get('duration', None)
        try:
            dur = int(dur)
        except (ValueError, TypeError):
            pass
        if (type(dur) != int) or (dur not in [30, 365]):
            raise serializers.ValidationError({"duration": "This value should be in [30, 365] days"})

        profile_id = self.context['request'].data.get('profile_id', None)
        try:
            profile_id = int(profile_id)
        except (ValueError, TypeError):
            pass
        if type(profile_id) != int:
            raise serializers.ValidationError({"profile_id": "This value should be int"})

        return obj


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        write_only_fields = ('password',)


class ProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    subscribe = SubscribeSerializer()

    class Meta:
        model = Profile
        fields = ('id', 'user', 'subscribe')

    def to_representation(self, instance):
        data = super(ProfileSerializer, self).to_representation(instance)
        user = data.pop('user')
        data['username'] = user.get('username')
        return data


class ProfileListSerializer(ProfileSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'user', 'subscribe')




