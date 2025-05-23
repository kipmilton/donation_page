# Generated by Django 5.1.6 on 2025-03-24 16:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_studentapplication_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsorselection',
            name='amount_contributed',
            field=models.DecimalField(decimal_places=2, default=10000, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sponsorselection',
            name='payment_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='studentapplication',
            name='amount_paid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='sponsorselection',
            name='sponsor_name',
            field=models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message='Only letters and spaces are allowed.', regex='^[A-Za-z ]+$')]),
        ),
        migrations.AlterField(
            model_name='studentapplication',
            name='name',
            field=models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message='Only letters and spaces are allowed.', regex='^[A-Za-z ]+$')]),
        ),
        migrations.AlterField(
            model_name='studentapplication',
            name='school',
            field=models.CharField(max_length=200, validators=[django.core.validators.RegexValidator(message='Only letters and spaces are allowed.', regex='^[A-Za-z ]+$')]),
        ),
    ]
