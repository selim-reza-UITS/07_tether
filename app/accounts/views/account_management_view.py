# Create your views here.
from rest_framework.generics import CreateAPIView
from app.accounts.serializers.signup_serializers import UserSignupSerializer,LoginSerializer
from app.accounts.serializers.profile_serializers import UserProfileSerializer
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()

class UserSignupView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer

    @swagger_auto_schema(
        operation_summary="Register a new user",
        operation_description="Signup using full name, email, mobile, and password.",
        request_body=UserSignupSerializer,
        responses={
            201: openapi.Response("User created successfully"),
            400: openapi.Response("Bad request (validation errors)")
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Handle user signup with validated serializer data.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):

    @swagger_auto_schema(
        request_body=LoginSerializer,
        operation_summary="User Login",
        operation_description="Login with email and password to get JWT tokens."
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)

        if hasattr(user, 'profile') and getattr(user.profile, 'status', '') == 'Suspended':
            return Response({"error": "Your account is suspended."}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)

        profile_data = {}
        if hasattr(user, 'profile'):
            profile_data = UserProfileSerializer(user.profile).data

        return Response({
            "message": "Login successful",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": profile_data
        }, status=status.HTTP_200_OK)