from django.contrib.auth.hashers import make_password
from django.db import IntegrityError

from rest_framework import serializers
from rest_framework.response import Response

import logging
logger = logging.getLogger(__name__)

from applicants.models import Applicant
from accountio.models import User
from common.choices import UserType
from employees.serializers import PublicUserSerializer

class PublicApplicantRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    user = PublicUserSerializer()  # Assuming you have defined PublicUserSerializer

    class Meta:
        model = Applicant
        fields = ['user', 'password', 'confirm_password', 'gender', 'skill_title']
        extra_kwargs = {
            'password': {'write_only': True}
        }

        def validate(self, attrs):
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')
            if password != confirm_password:
                raise serializers.ValidationError({"Error": ["Passwords do not match!"]})
            return attrs


    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError({"Error": ["Passwords do not match!"]})
        user = User.objects.create_user(**user_data, password=password, type=UserType.APPLICANT)
        Applicant.objects.create(user=user,password=make_password(password), **validated_data)
        return user

    def to_representation(self, instance):
        payload = {"message": f"Registration successful for {instance.username}."}
        return payload

    
class PublicApplicantLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(max_length=228)
    class Meta:
        model = User
        fields = ["email", "password"]
        
class PrivateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','username','name', 'phone', 'type']

class PrivateApplicantProfileSerializer(serializers.ModelSerializer):
    user = PrivateUserSerializer()

    class Meta:
        model = Applicant
        fields = ["uid", "user", 'gender', 'skill_title']
        
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = PrivateUserSerializer(instance.user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
            else:
                raise serializers.ValidationError(user_serializer.errors)

        return super().update(instance, validated_data)