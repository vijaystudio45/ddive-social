# Generated by Django 5.0.2 on 2024-06-20 07:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('post_date', models.DateTimeField(blank=True, null=True)),
                ('image', models.ImageField(upload_to='images/')),
                ('option', models.CharField(choices=[('LinkedIn', 'LinkedIn'), ('Instagram', 'Instagram'), ('Facebook', 'Facebook')], max_length=10)),
                ('description', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('page_id', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GeneratePost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('post_date', models.DateTimeField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('channel', models.CharField(choices=[('LinkedIn', 'LinkedIn'), ('Instagram', 'Instagram'), ('Facebook', 'Facebook')], max_length=10)),
                ('description', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('page_id', models.CharField(blank=True, max_length=100, null=True)),
                ('linkedin_page_id', models.CharField(blank=True, max_length=100, null=True)),
                ('linkedin_page_video_id', models.CharField(blank=True, max_length=100, null=True)),
                ('linkedin_page_image_id', models.CharField(blank=True, max_length=100, null=True)),
                ('image_needed', models.BooleanField(blank=True, default=False, null=True)),
                ('image_needed_prompt', models.CharField(blank=True, max_length=100, null=True)),
                ('generated_image', models.CharField(blank=True, max_length=600, null=True)),
                ('post_status', models.CharField(blank=True, choices=[('Approve', 'Approve'), ('Inprogress', 'Inprogress'), ('Live', 'Live')], default='Inprogress', max_length=10, null=True)),
                ('generated_fb_post', models.TextField(blank=True, null=True)),
                ('generated_insta_post', models.TextField(blank=True, null=True)),
                ('generated_linkedin_post', models.TextField(blank=True, null=True)),
                ('facebook_page_post_id', models.CharField(blank=True, max_length=100, null=True)),
                ('instagram_page_post_id', models.CharField(blank=True, max_length=100, null=True)),
                ('instagram_page_video_id', models.CharField(blank=True, max_length=100, null=True)),
                ('fb_page_video_id', models.CharField(blank=True, max_length=100, null=True)),
                ('fb_video', models.FileField(blank=True, null=True, upload_to='videos/')),
                ('fb_page_name', models.CharField(blank=True, max_length=100, null=True)),
                ('linkedin_page_name', models.CharField(blank=True, max_length=100, null=True)),
                ('Instagram_page_id', models.CharField(blank=True, max_length=100, null=True)),
                ('Instagram_page_name', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='generate_user', to='authentication.customuser')),
            ],
        ),
        migrations.CreateModel(
            name='UserAccessToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=4000)),
                ('types', models.CharField(choices=[('LinkedIn', 'LinkedIn'), ('Instagram', 'Instagram'), ('Facebook', 'Facebook')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('page_access_token', models.CharField(blank=True, max_length=4000, null=True)),
                ('page_id', models.CharField(blank=True, max_length=4000, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_access_token', to='authentication.customuser')),
            ],
        ),
    ]