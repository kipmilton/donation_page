# Generated by Django 5.1.6 on 2025-03-08 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentapplication',
            name='supportive_documents',
            field=models.FileField(blank=True, null=True, upload_to='supportive_documents/'),
        ),
    ]
