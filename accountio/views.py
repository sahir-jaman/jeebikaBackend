from rest_framework.generics import ListCreateAPIView
from rest_framework import status
from rest_framework.response import Response

from .models import User 
from .serializers import PublicUserRegistrationSerializer


class PublicUserRegistration(ListCreateAPIView):
    serializer_class = PublicUserRegistrationSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            # Use the custom user manager to create a user with a hashed password
            user = User.objects.create_user(email=email, password=password)

            return Response({'status': 'Registration successful'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)