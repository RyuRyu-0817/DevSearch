# Generated by Django 4.2.6 on 2024-01-12 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pevsearch', '0003_profile_remove_customuser_picture_delete_comment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
