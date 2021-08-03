from django.core.validators import RegexValidator
from django.db import models, transaction
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework.authtoken.models import Token

from user_profile.helpers import generate_code


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="user_profile", on_delete=models.CASCADE)

    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)

    card_number = models.CharField(max_length=255, blank=True, null=True)
    sheba_number = models.CharField(max_length=255, blank=True, null=True)

    phone_number = models.CharField(max_length=12, validators=[
        RegexValidator(
            regex=r"^(\+98|0)?9\d{9}$",
            message=_("Enter a valid phone number"),
            code='invalid_phone_number'
        ),
    ], unique=True)
    national_code = models.CharField(max_length=15, blank=True, null=True)

    PENDING = '0'
    VERIFIED = '1'
    REJECTED = '2'

    verification_states = (
        (PENDING, _("Pending")),
        (VERIFIED, _("Verified")),
        (REJECTED, _("Rejected")),
    )

    verification_status = models.CharField(max_length=1, choices=verification_states, default=PENDING)

    def get_verification_object(self):
        return UserProfilePhoneVerification.objects.create(user_profile=self)

    def __str__(self):
        return "%d - %s - %s %s" % (self.pk, self.phone_number, self.first_name, self.last_name)

    @property
    def token(self):
        token, created = Token.objects.get_or_create(user=self.user)
        return token.key


class UserProfilePhoneVerificationObjectManager(models.Manager):

    def _get_or_create(self, **kwargs):
        created = False
        user_profile = kwargs.get('user_profile')
        verification_object = self.last_not_expired_verification_object(user_profile)
        if not verification_object:
            # create a new object if none exists
            verification_object = UserProfilePhoneVerification(**kwargs)
            verification_object.save()
            created = True

        return created, verification_object

    def create(self, **kwargs):
        with transaction.atomic():
            user_profile = kwargs.get('user_profile')

            # lock the user profile to prevent concurrent creations
            user_profile = UserProfile.objects.select_for_update().get(pk=user_profile.pk)

            created, verification_object = self._get_or_create(user_profile=user_profile)

            if created:
                return {'status': 201, 'obj': verification_object}

            # only one valid verification object at a time
            return {
                'status': 403,
                'wait': self.remaining_time_until_next_verification_object_can_be_created(verification_object)
            }

    @staticmethod
    def last_not_expired_verification_object(user_profile):
        time = timezone.now() - timezone.timedelta(minutes=UserProfilePhoneVerification.RETRY_TIME)
        # select the latest valid user profile phone verification object
        user_profile_phone = UserProfilePhoneVerification.objects.order_by('-create_date'). \
            filter(create_date__gte=time,
                   user_profile__phone_number=user_profile.phone_number) \
            .last()

        if user_profile_phone and user_profile_phone.is_usable:
            return user_profile_phone

    @staticmethod
    def remaining_time_until_next_verification_object_can_be_created(user_profile_phone):
        return timezone.timedelta(minutes=UserProfilePhoneVerification.RETRY_TIME) + \
               (user_profile_phone.create_date - timezone.now())


class UserProfilePhoneVerification(models.Model):
    """
        Used for phone verification by sms
        auto generates a 5 digit code
        limits select querying
        time intervals between consecutive creation
    """

    RETRY_TIME = 1
    MAX_QUERY = 5

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="phone_numbers")
    code = models.CharField(max_length=13, default=generate_code)
    create_date = models.DateTimeField(auto_now_add=True)
    query_times = models.IntegerField(default=0)
    used = models.BooleanField(default=False)
    burnt = models.BooleanField(default=False)

    objects = UserProfilePhoneVerificationObjectManager()

    @property
    def is_usable(self):
        return not self.used and not self.burnt and self.query_times <= UserProfilePhoneVerification.MAX_QUERY
