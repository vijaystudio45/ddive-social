# Generated by Django 5.0.2 on 2024-05-20 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_alter_category_options_alter_staticprompts_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='voucher',
            name='user',
        ),
        migrations.AddField(
            model_name='voucher',
            name='is_used',
            field=models.BooleanField(default=False),
        ),
    ]
