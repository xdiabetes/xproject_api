# Generated by Django 2.2.4 on 2020-03-05 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0009_auto_20200305_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='block_code',
            field=models.CharField(blank=True, help_text='Block Code', max_length=20, null=True, verbose_name='Block Code'),
        ),
    ]
