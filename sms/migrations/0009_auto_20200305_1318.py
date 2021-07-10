# Generated by Django 2.2.4 on 2020-03-05 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0008_auto_20200305_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operator',
            name='api_key',
            field=models.CharField(blank=True, help_text='API key given by operator', max_length=255, null=True, verbose_name='API Key'),
        ),
        migrations.AlterField(
            model_name='operator',
            name='template',
            field=models.CharField(blank=True, help_text='template given by operator', max_length=255, null=True, verbose_name='Template'),
        ),
    ]
