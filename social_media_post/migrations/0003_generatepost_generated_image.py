# Generated by Django 5.0.2 on 2024-03-08 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_media_post', '0002_generatepost'),
    ]

    operations = [
        migrations.AddField(
            model_name='generatepost',
            name='generated_image',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]
