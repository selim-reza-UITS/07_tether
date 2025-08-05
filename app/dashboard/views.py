from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken  # JWT

from app.accounts.models import User
from app.dashboard.serializers.accounts_serializers import (
    AdminLoginSerializer, UserSerializer)
from app.dashboard.serializers.terms_and_policy import (
    AboutUsSerializer, PrivacyPolicySerializer, TermsConditionsSerializer)

from .models import AboutUs, PrivacyPolicy, TermsConditions


class PrivacyPolicyView(generics.RetrieveUpdateAPIView):
    queryset = PrivacyPolicy.objects.all()
    serializer_class = PrivacyPolicySerializer

    def get_object(self):
        return PrivacyPolicy.objects.first()

class TermsConditionsView(generics.RetrieveUpdateAPIView):
    queryset = TermsConditions.objects.all()
    serializer_class = TermsConditionsSerializer

    def get_object(self):
        return TermsConditions.objects.first()
    
class AboutUsView(generics.RetrieveAPIView):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer

    def get_object(self):
        return AboutUs.objects.first()



@api_view(["POST"])
def contact_us(request):
    user = request.user
    message = request.data.get("message")

    # Validate inputs
    if not all([message]):
        return Response(
            {"message": None, "error": "All fields except phone are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    context = {
        "email": user.email,
        "message": message,
    }

    subject = f"New message from {user.email}"
    body_html = render_to_string('email/contact.html', context)

    try:
        email_msg = EmailMultiAlternatives(
            subject=subject,
            body=f"Message from {user.email}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.EMAIL_HOST_USER]
        )
        email_msg.attach_alternative(body_html, "text/html")
        email_msg.send()
    except Exception as e:
        return Response(
            {"message": None, "error": f"Failed to send email: {str(e)}","status":status.HTTP_400_BAD_REQUEST},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return Response(
        {"message": "Your message has been sent successfully.", "error": None,"status":status.HTTP_200_OK},
        status=status.HTTP_200_OK
    )






class AdminLoginView(APIView):
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'full_name': user.full_name,
                    'is_staff': user.is_staff
                }
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserManagementListView(generics.ListAPIView):
    # queryset = User.objects.select_related('profile').all().order_by('full_name')
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class UserManagementDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response({"detail": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)