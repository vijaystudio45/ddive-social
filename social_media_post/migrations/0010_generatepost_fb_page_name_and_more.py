# Generated by Django 5.0.2 on 2024-03-15 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_media_post', '0009_generatepost_fb_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='generatepost',
            name='fb_page_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='generatepost',
            name='linkedin_page_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]