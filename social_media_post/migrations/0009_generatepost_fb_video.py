# Generated by Django 5.0.2 on 2024-03-13 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_media_post', '0008_generatepost_linkedin_page_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='generatepost',
            name='fb_video',
            field=models.FileField(blank=True, null=True, upload_to='videos/'),
        ),
    ]