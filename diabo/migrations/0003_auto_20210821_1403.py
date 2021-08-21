# Generated by Django 3.2.6 on 2021-08-21 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0001_initial'),
        ('diabo', '0002_auto_20210821_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diaboprofile',
            name='job',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='job.job'),
        ),
        migrations.DeleteModel(
            name='Job',
        ),
    ]