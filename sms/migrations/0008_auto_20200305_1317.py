# Generated by Django 2.2.4 on 2020-03-05 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0007_auto_20191010_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='operator',
            name='api_key',
            field=models.CharField(blank=True, help_text='API key given by operator', max_length=255, null=True, verbose_name='Token'),
        ),
        migrations.AddField(
            model_name='operator',
            name='template',
            field=models.CharField(blank=True, help_text='template given by operator', max_length=255, null=True, verbose_name='Token'),
        ),
        migrations.AddField(
            model_name='operator',
            name='vendor',
            field=models.CharField(choices=[('0', 'Faraz SMS'), ('1', 'Kavenegar')], default='0', max_length=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='operator',
            name='password',
            field=models.CharField(blank=True, help_text='Password given by operator', max_length=255, null=True, verbose_name='Password'),
        ),
        migrations.AlterField(
            model_name='operator',
            name='sender',
            field=models.CharField(blank=True, help_text='The operator phone number', max_length=15, null=True, verbose_name='Sender Phone Number'),
        ),
        migrations.AlterField(
            model_name='operator',
            name='username',
            field=models.CharField(blank=True, help_text='User name given by operator', max_length=255, null=True, verbose_name='Username'),
        ),
    ]