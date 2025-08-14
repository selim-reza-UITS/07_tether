from rest_framework import generics, permissions
from .models import Subscription
from .serializers import SubcriptionsSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# 1️⃣ USER VIEW — only active packages
class ActiveSubscriptionListView(generics.ListAPIView):
    queryset = Subscription.objects.filter(status=True)
    serializer_class = SubcriptionsSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_summary="List Active Subscriptions",
        operation_description="Returns a list of active subscription packages available to users.",
        responses={200: SubcriptionsSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


# 2️⃣ ADMIN VIEW — list + create
class SubscriptionListCreateView(generics.ListCreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubcriptionsSerializer
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        operation_summary="List All Subscriptions (Admin)",
        operation_description="Returns all subscriptions, active and inactive.",
        responses={200: SubcriptionsSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create Subscription (Admin)",
        operation_description="Creates a new subscription package. Admin only.",
        request_body=SubcriptionsSerializer,
        responses={201: SubcriptionsSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# 3️⃣ ADMIN PARTIAL UPDATE
class SubscriptionPartialUpdateView(generics.UpdateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubcriptionsSerializer
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ['patch']

    @swagger_auto_schema(
        operation_summary="Update Subscription (Partial, Admin)",
        operation_description="Partially updates a subscription. Only Admins can perform this.",
        request_body=SubcriptionsSerializer,
        responses={200: SubcriptionsSerializer}
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
