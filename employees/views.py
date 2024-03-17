from django.shortcuts import render
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate

from rest_framework.generics import get_object_or_404, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.filters import SearchFilter

from .serializers import PublicEmployeeRegistrationSerializer, PrivateEmployeeProfileSerializer, PublicEmployeeLoginSerializer, PrivateEmployeePostSerializer
from accountio.models import User
from common.permissions import IsEmployeeUser
from .models import Employee, job_post


class PublicEmployeeRegistrationView(CreateAPIView):
    serializer_class = PublicEmployeeRegistrationSerializer
        
class PublicEmployeeLogin(CreateAPIView):
    serializer_class = PublicEmployeeLoginSerializer

    def generate_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        _email = serializer.validated_data['email']
        _password = serializer.validated_data['password']

        try:
            user = User.objects.get(email__iexact=_email)  # Case-insensitive email comparison

            if not check_password(_password, user.password):
                raise AuthenticationFailed()

            tokens = self.generate_tokens_for_user(user)

            return Response({'tokens': tokens, 'status': 'Login successful'}, status=status.HTTP_201_CREATED)
            
        except User.DoesNotExist:
            raise AuthenticationFailed()
        
        
class PrivateEmployeeProfile(RetrieveUpdateAPIView):
    serializer_class = PrivateEmployeeProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Access the related Employee object of the current user
        employee = self.request.user.employee
        return employee

    def update(self, request, *args, **kwargs):
        # Ensure that only PATCH requests are allowed
        if request.method != 'PATCH':
            return Response({'error': 'Only GET & PATCH method is allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        # Retrieve the Employee object
        instance = self.get_object()
        
        # Serialize the instance with data from the request
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)
    
    
class PrivateEmployeeposts(ListCreateAPIView):
    serializer_class = PrivateEmployeePostSerializer
    permission_classes = [IsAuthenticated, IsEmployeeUser]
    filter_backends = [SearchFilter]
    search_fields = ["category__name"]
    
    queryset = job_post.objects.all()
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PrivateEmployeePostDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = PrivateEmployeePostSerializer
    permission_classes = [IsAuthenticated, IsEmployeeUser]
    queryset = job_post.objects.all()
    
    def get_object(self):
        uid = self.kwargs.get("post_uid", None)
        
        return get_object_or_404(
            job_post.objects.filter(), uid=uid
        )

    

    
