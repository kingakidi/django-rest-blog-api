from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from .models import User
from .serializers import (
    UserSignupSerializer, 
    UserLoginSerializer, 
    UserSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer
)
from .models import PasswordResetOTP
from .utils import send_password_reset_otp


class UserSignupView(APIView):
    @extend_schema(
        tags=['Auth'],
        summary="User Registration",
        description="Register a new user account",
        request=UserSignupSerializer,
        responses={
            201: {
                'type': 'object',
                'properties': {
                    'user': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'email': {'type': 'string'},
                            'first_name': {'type': 'string'},
                            'last_name': {'type': 'string'},
                            'date_joined': {'type': 'string', 'format': 'date-time'}
                        }
                    },
                    'tokens': {
                        'type': 'object',
                        'properties': {
                            'refresh': {'type': 'string'},
                            'access': {'type': 'string'}
                        }
                    }
                }
            },
            400: "Bad Request - Validation errors"
        }
    )
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)
            
            return Response({
                'user': user_serializer.data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    @extend_schema(
        tags=['Auth'],
        summary="User Login",
        description="Authenticate user and return JWT tokens",
        request=UserLoginSerializer,
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'user': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'email': {'type': 'string'},
                            'first_name': {'type': 'string'},
                            'last_name': {'type': 'string'},
                            'date_joined': {'type': 'string', 'format': 'date-time'}
                        }
                    },
                    'tokens': {
                        'type': 'object',
                        'properties': {
                            'refresh': {'type': 'string'},
                            'access': {'type': 'string'}
                        }
                    }
                }
            },
            400: "Bad Request - Invalid credentials"
        }
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)
            
            return Response({
                'user': user_serializer.data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenRefreshView(APIView):
    @extend_schema(
        tags=['Auth'],
        summary="Refresh JWT Token",
        description="Get a new access token using refresh token",
        request={
            'type': 'object',
            'properties': {
                'refresh': {'type': 'string'}
            },
            'required': ['refresh']
        },
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'access': {'type': 'string'}
                }
            },
            400: "Bad Request - Invalid refresh token"
        }
    )
    def post(self, request):
        refresh_token = request.data.get('refresh')
        
        if not refresh_token:
            return Response(
                {'error': 'Refresh token is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            
            return Response({
                'access': access_token
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': 'Invalid refresh token'}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class PasswordResetRequestView(APIView):
    @extend_schema(
        tags=['Auth'],
        summary="Request Password Reset",
        description="Send OTP to user's email for password reset",
        request=PasswordResetRequestSerializer,
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'email': {'type': 'string'}
                }
            },
            400: "Bad Request - Invalid email"
        }
    )
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            
            otp = PasswordResetOTP.create_otp(user)
            email_sent = send_password_reset_otp(user, otp.otp_code)
            
            if email_sent:
                return Response({
                    'message': 'OTP sent successfully to your email',
                    'email': email
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Failed to send OTP email. Please try again.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    @extend_schema(
        tags=['Auth'],
        summary="Confirm Password Reset",
        description="Reset password using OTP code",
        request=PasswordResetConfirmSerializer,
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            },
            400: "Bad Request - Invalid OTP or validation errors"
        }
    )
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_code = serializer.validated_data['otp_code']
            new_password = serializer.validated_data['new_password']
            
            try:
                user = User.objects.get(email=email)
                
                otp = PasswordResetOTP.objects.filter(
                    user=user,
                    otp_code=otp_code,
                    is_used=False
                ).first()
                
                if not otp:
                    return Response({
                        'error': 'Invalid OTP code'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                if not otp.is_valid():
                    return Response({
                        'error': 'OTP has expired. Please request a new one.'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                user.set_password(new_password)
                user.save()
                otp.is_used = True
                otp.save()
                
                return Response({
                    'message': 'Password reset successfully'
                }, status=status.HTTP_200_OK)
                
            except User.DoesNotExist:
                return Response({
                    'error': 'User not found'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
