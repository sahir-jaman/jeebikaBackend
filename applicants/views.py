from django.contrib.auth.hashers import check_password

from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

from .serializers import PublicApplicantRegistrationSerializer, PrivateApplicantProfileSerializer, PublicApplicantLoginSerializer
from accountio.models import User
from .models import Applicant



class PublicUserRegistrationView(CreateAPIView):
    # queryset = Applicant.objects.all()
    serializer_class = PublicApplicantRegistrationSerializer
        

class PublicUserLoginView(CreateAPIView):
    queryset = Applicant.objects.all()
    serializer_class = PublicApplicantLoginSerializer

    def generate_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return access_token, refresh_token
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        _email = serializer.validated_data['email']
        _password = serializer.validated_data['password']

        try:
            user = User.objects.get(email__iexact=_email)  # Case-insensitive email comparison

            if not check_password(_password, user.password):
                raise AuthenticationFailed()

            access_token, refresh_token = self.generate_tokens_for_user(user)

            # Set cookies
            response = Response({'tokens': {'access': access_token, 'refresh': refresh_token}, 'status': 'Login successful'}, status=status.HTTP_201_CREATED)
            response.set_cookie('refresh_token', refresh_token, httponly=True)
            
            return response
            
        except User.DoesNotExist:
            raise AuthenticationFailed()




class PrivateApplicantProfile(RetrieveUpdateAPIView):
    serializer_class = PrivateApplicantProfileSerializer
    permission_classes = [IsAuthenticated]
        
    def get_object(self):
        applicant = self.request.user.applicant
        return applicant
    
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
        
        
        