from app.accounts.serializers.profile_serializers import UserProfileSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status,permissions
from rest_framework.views import APIView


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(
        operation_summary="Get user profile",
        responses={200: UserProfileSerializer()}
    )
    def get(self, request):
        profile = request.user.profile
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_summary="Update user profile",
        request_body=UserProfileSerializer,
        responses={200: UserProfileSerializer()}
    )
    def patch(self, request):
        profile = request.user.profile
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)