# Generated by Django 4.0.5 on 2022-06-30 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LstStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=100)),
                ('word', models.CharField(max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='GetMails',
        ),
    ]
