from rest_framework import serializers
from .models import Subscription


class SubcriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = [
            "package_amount",
            "package_type",
            "status",
        ]
        read_only_fields = [
            "package_id","created_at","updated_at",
        ]        