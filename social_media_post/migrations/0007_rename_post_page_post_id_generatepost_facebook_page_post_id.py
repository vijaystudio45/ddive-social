# Generated by Django 5.0.2 on 2024-03-08 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_media_post', '0006_generatepost_post_page_post_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='generatepost',
            old_name='post_page_post_id',
            new_name='facebook_page_post_id',
        ),
    ]
