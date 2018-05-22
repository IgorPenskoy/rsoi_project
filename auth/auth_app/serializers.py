from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

UserModel = get_user_model()


class GroupRegisterSerializer(RegisterSerializer):
    group = serializers.CharField(max_length=30, required=True)

    def validate_group(self, group):
        try:
            self.group_obj = Group.objects.get(name=group)
        except Group.DoesNotExist:
            raise serializers.ValidationError(_("Group %s not exist." % group))

    def custom_signup(self, request, user):
        user.groups.add(self.group_obj)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('pk', 'name',)
        read_only_fields = ('pk', 'name',)


class CustomUserDetailsSerializer(UserDetailsSerializer):
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = UserModel
        fields = ('pk', 'username', 'email', 'first_name', 'last_name', 'groups',)
        read_only_fields = ('email', 'groups',)
