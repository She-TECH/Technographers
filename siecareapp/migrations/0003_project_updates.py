# Generated by Django 2.1.3 on 2020-03-05 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siecareapp', '0002_policies'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project_updates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(default='NULL', max_length=255)),
                ('department', models.CharField(default='NULL', max_length=255)),
                ('information', models.CharField(default='NULL', max_length=255)),
            ],
        ),
    ]
