from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework.authtoken.models import Token

from xapp.api_v1.consts import (UserProfileConsts)
from xapp.api_v1.helpers import generate_code, send_verification_code


class UserProfile(models.Model):
    """
        User Profile object, one to one with django user
        additional info about the user
    """

    django_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")

    first_name = models.CharField(max_length=255, default="")
    last_name = models.CharField(max_length=255, default="")
    nick_name = models.CharField(max_length=255, default="")

    phone_number = models.CharField(max_length=12, validators=[
        RegexValidator(
            regex=r"^(\+98|0)?9\d{9}$",
            message=_("Enter a valid phone number"),
            code='invalid_phone_number'
        ),
    ], unique=True)

    email = models.EmailField(max_length=255, blank=True, null=True)

    verification_status = models.CharField(max_length=1, choices=UserProfileConsts.states,
                                           default=UserProfileConsts.PENDING)

    @property
    def base_addresses(self):
        return self.addresses.filter(is_clone=False)

    @property
    def balance(self) -> int:
        return self.wallet.balance

    @property
    def has_usable_password(self):
        return self.django_user.has_usable_password()

    @property
    def token(self):
        token, created = Token.objects.get_or_create(user=self.django_user)
        return token.key

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    @property
    def date_joined(self):
        return self.django_user.date_joined

    @property
    def cafe_relations_no_sms(self):
        return self.cafe_relations.exclude(role__code_name="PAYMENT_NOTIFY")

    def __str__(self):
        return "%s (%s)" % (self.django_user.username, self.full_name)


class UserProfilePhoneVerificationObjectManager(models.Manager):
    def create(self, **kwargs):
        created = False

        with transaction.atomic():
            user_profile = kwargs.get('user_profile')

            # lock the user profile to prevent concurrent creations
            user_profile = UserProfile.objects.select_for_update().get(pk=user_profile.pk)

            time = timezone.now() - timezone.timedelta(minutes=UserProfilePhoneVerification.RETRY_TIME)

            # select the latest valid user profile phone verification object
            user_profile_phone = UserProfilePhoneVerification.objects.order_by('-create_date'). \
                filter(create_date__gte=time,
                       user_profile__phone_number=user_profile.phone_number) \
                .last()

            # create a new object if none exists
            if not user_profile_phone:
                obj = UserProfilePhoneVerification(**kwargs)
                obj.save()
                created = True

        if created:
            return {'status': 201, 'obj': obj}

        return {
            'status': 403,
            'wait': timezone.timedelta(minutes=UserProfilePhoneVerification.RETRY_TIME) +
                    (user_profile_phone.create_date - timezone.now())}


class UserProfilePhoneVerification(models.Model):
    """
        Used for phone verification by sms
        auto generates a 5 digit code
        limits select querying
        time intervals between consecutive creation
    """

    RETRY_TIME = 0
    MAX_QUERY = 5

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="phone_numbers")
    code = models.CharField(max_length=13, default=generate_code)
    create_date = models.DateTimeField(auto_now_add=True)
    query_times = models.IntegerField(default=0)
    used = models.BooleanField(default=False)
    burnt = models.BooleanField(default=False)

    objects = UserProfilePhoneVerificationObjectManager()


@receiver(post_save, sender=UserProfilePhoneVerification)
def send_verification_sms(sender, instance, created, **kwargs):
    """
        send the verification code if a new object is created
    """

    if created:
        send_verification_code(instance.user_profile.phone_number, instance.code)

