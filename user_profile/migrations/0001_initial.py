# Generated by Django 3.2.3 on 2021-05-14 11:17

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import user_profile.helpers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=12, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_phone_number', message='Enter a valid phone number', regex='^(\\+98|0)?9\\d{9}$')])),
                ('national_code', models.CharField(blank=True, max_length=15, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfilePhoneVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default=user_profile.helpers.generate_code, max_length=13)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('query_times', models.IntegerField(default=0)),
                ('used', models.BooleanField(default=False)),
                ('burnt', models.BooleanField(default=False)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phone_numbers', to='user_profile.userprofile')),
            ],
        ),
    ]
