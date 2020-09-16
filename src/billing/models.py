import stripe
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save

from accounts.models import GuestEmail
User = settings.AUTH_USER_MODEL

# abc@teamcfe.com -->> 1000000 billing profiles
# user abc@teamcfe.com -- 1 billing profile

stripe.api_key = "sk_test_51HQwJDE9dKyATRmBfqOTCDB0lrrbYsQ402TLCd9iKBXkmrB4O7Ct3nVkjxK9HiW5Ren13woNiRCnx9lft3HX9Zr000oke1IFQH"


class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        guest_email_id = request.session.get('guest_email_id')
        created = False
        obj = None
        if user.is_authenticated():
            'logged in user checkout; remember payment stuff'
            obj, created = self.model.objects.get_or_create(
                user=user, email=user.email)
        elif guest_email_id is not None:
            'guest user checkout; auto reloads payment stuff'
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            obj, created = self.model.objects.get_or_create(
                email=guest_email_obj.email)
        else:
            pass
        return obj, created


class BillingProfile(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    customer_id = models.CharField(max_length=120, null=True, blank=True)
    # customer_id in Stripe or Braintree

    objects = BillingProfileManager()

    def __str__(self):
        return self.email


def billing_profile_created_receiver(sender, instance, *args, **kwargs):
    if not instance.customer_id and instance.email:
        print("ACTUAL API REQUEST Send to stripe/braintree")
        customer = stripe.Customer.create(
            email=instance.email
        )
        print(customer)
        instance.customer_id = customer.id


pre_save.connect(billing_profile_created_receiver, sender=BillingProfile)


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(
            user=instance, email=instance.email)


post_save.connect(user_created_receiver, sender=User)


class CardManager(models.Manager):
    def add_new(self, billing_profile, stripe_card_response):
        if str(stripe_card_response.object) == "customer":
            new_card = self.model(
                billing_profile=billing_profile,
                stripe_id=stripe_card_response.id,
                currency=stripe_card_response.currency,
                country=stripe_card_response.livemode,
                exp_month=stripe_card_response.balance,
                exp_year=stripe_card_response.balance,
                last4=stripe_card_response.balance
            )
            new_card.save()
            return new_card
        return None


class Card(models.Model):
    billing_profile = models.ForeignKey(
        BillingProfile, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=120)
    currency = models.CharField(max_length=120, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    exp_month = models.IntegerField(null=True, blank=True)
    exp_year = models.IntegerField(null=True, blank=True)
    last4 = models.CharField(max_length=4, null=True, blank=True)
    default = models.BooleanField(default=True)

    objects = CardManager()

    def __str__(self):
        return "{} {}".format(self.currency, self.stripe_id)


class ChargeManager(models.Manager):

    def do(self, billing_profile, order_obj, card=None):
        card_obj = card
        if card_obj is None:
            cards = billing_profile.card_set.filter(default=True)
            if card.exists():
                card_obj = cards.first()
        if card is None:
            return False, "No cards available"
        c = stripe.Charge.create(
            amount=int(order_obj.total * 100),
            currency="NPR",
            customer=BillingProfile.customer_id,
            description="Charge for someone@noone.com",
            metadata={"order_id": order_obj.order_id}
        )
        new_charge_obj = self.model(
            billing_profile=billing_profile,
            stripe_id=c.id,
            paid=c.paid,
            refunded=c.refunded,
            brand=c.payment_method_details.get('brand'),
            status=c.status,
            created=c.created,
        )
        new_charge_obj.save()
        return new_charge_obj.paid, new_charge_obj.brand


class Charge(models.Model):
    billing_profile = models.ForeignKey(BillingProfile,on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=120, null=True, blank=True)
    paid = models.BooleanField(default=False)
    refunded = models.BooleanField(default=False)
    brand = models.CharField(max_length=120, blank=True, null=True)
    status = models.CharField(max_length=120, null=True, blank=True)
    created = models.IntegerField(blank=True, null=True)

    objects = ChargeManager()