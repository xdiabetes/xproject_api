# Generated by Django 3.2.6 on 2021-08-20 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diabetes_therapy', '0003_rename_therapytype_therapycategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='fixtherapy',
            name='visibility',
            field=models.CharField(choices=[('0', 'Public'), ('1', 'Private')], default='1', max_length=1),
        ),
        migrations.AddField(
            model_name='withmealtherapy',
            name='visibility',
            field=models.CharField(choices=[('0', 'Public'), ('1', 'Private')], default='1', max_length=1),
        ),
    ]
