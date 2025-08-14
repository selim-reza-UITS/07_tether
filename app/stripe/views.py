import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
from app.accounts.models import User,UserProfile
from app.subscribtions.models import Subscription
stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET 

class CreateStripeCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        package_id = request.data.get("package_id")
        if not package_id:
            return Response({"error": "package_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            subscription_package = Subscription.objects.get(package_id=package_id, status=True)
        except Subscription.DoesNotExist:
            return Response({"error": "Subscription package not found or inactive."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        try:
            # Stripe expects amount in cents, price as integer
            price_in_cents = subscription_package.package_amount * 100

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",  # adjust currency as needed
                            "unit_amount": price_in_cents,
                            "product_data": {
                                "name": f"{subscription_package.package_type} Subscription",
                            },
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",  # one-time payment mode
                success_url="http://localhost:3000/success",
                cancel_url="http://localhost:3000/cancel",
                metadata={
                    "user_id": str(user.id),
                    "package_id": package_id,
                    "payment_for": "subscription",
                },
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"checkout_url": checkout_session.url})
    
    
    
    
    
class CancelSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        profile = getattr(user, "profile", None)

        if not profile:
            return Response({"error": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)

        # Get the free subscription plan
        free_plan = Subscription.objects.filter(
            package_type=Subscription.PackageType.FREE,
            status=True
        ).first()

        if not free_plan:
            return Response({"error": "Free subscription plan not configured."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Downgrade user subscription to free
        profile.subscription_plan = free_plan
        profile.subscription_start = None
        profile.subscription_end = None
        profile.save()

        return Response({"message": "Subscription canceled and downgraded to free plan."}, status=status.HTTP_200_OK)






@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        metadata = session.get('metadata', {})
        user_id = metadata.get('user_id')
        package_id = metadata.get('package_id')
        payment_for = metadata.get('payment_for')

        if payment_for != "subscription":
            return HttpResponse(status=200)  # Ignore non-subscription payments here

        try:
            user = User.objects.get(id=user_id)
            profile = user.profile
            subscription = Subscription.objects.get(package_id=package_id, status=True)

            # Update subscription info on profile
            profile.subscription_plan = subscription
            profile.subscription_start = timezone.now()

            # Set expiry based on package_type
            if subscription.package_type == Subscription.PackageType.MONTHLY:
                profile.subscription_end = timezone.now() + timedelta(days=30)
            elif subscription.package_type == Subscription.PackageType.YEARLY:
                profile.subscription_end = timezone.now() + timedelta(days=365)
            else:
                profile.subscription_end = None  # Free or no expiry

            profile.save()

        except (User.DoesNotExist, UserProfile.DoesNotExist, Subscription.DoesNotExist):
            # Log error or handle gracefully
            return HttpResponse(status=400)

    # You can handle other event types here if needed

    return HttpResponse(status=200)
