from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _


class GroupRegisterSerializer(RegisterSerializer):
    group = serializers.CharField(max_length=30, required=True)

    def validate_group(self, group):
        try:
            self.group_obj = Group.objects.get(name=group)
        except Group.DoesNotExist:
            raise serializers.ValidationError(_("Group %s not exist." % group))

    def custom_signup(self, request, user):
        user.groups.add(self.group_obj)
