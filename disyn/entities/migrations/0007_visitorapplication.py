# Generated by Django 5.1 on 2024-08-17 13:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0006_upvote_name_upvote_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='VisitorApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('application_type', models.CharField(choices=[('visit', 'Visit'), ('internship', 'Internship'), ('job', 'Job')], max_length=10)),
                ('message', models.TextField()),
                ('cv', models.FileField(blank=True, null=True, upload_to='visitor_cvs/')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visitor_applications', to='entities.entity')),
            ],
        ),
    ]
