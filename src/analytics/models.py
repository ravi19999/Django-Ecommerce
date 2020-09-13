from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.db.models.signals import pre_save, post_save
from django.db import models

from accounts.signals import user_logged_in
from .signals import object_viewed_signal
from .utils import get_client_ip

User = settings.AUTH_USER_MODEL


class ObjectViewed(models.Model):
    # User instance instance.id
    user = models.ForeignKey(User, blank=True, null=True)
    ip_address = models.CharField(
        max_length=220, blank=True, null=True)  # IP Field
    # User, Product, Order, Cart, Address
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()  # User id, Product id, Order id,
    content_object = GenericForeignKey(
        'content_type', 'object_id')  # Product instance
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s viewed on %s" % (self.content_object, self.timestamp)

    class Meta:
        ordering = ['-timestamp']  # most recent saved show up first
        verbose_name = 'Object viewed'
        verbose_name_plural = 'Objects viewed'


def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender)  # instance.__class__
    new_view_obj = ObjectViewed.objects.create(
        user=request.user,
        content_type=c_type,
        object_id=instance.id,
        ip_address=get_client_ip(request)
    )


object_viewed_signal.connect(object_viewed_receiver)


class UserSession(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    ip_address = models.CharField(
        max_length=220, blank=True, null=True)  # IP Field
    timestamp = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField(default=True)
    ended = models.BooleanField(default=False)


def user_logged_in_receiver(sender, instance, request, *args, **kwargs):
    print(instance)


user_logged_in.connect(user_logged_in_receiver)
