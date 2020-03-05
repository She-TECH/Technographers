# Generated by Django 2.1.3 on 2020-03-05 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siecareapp', '0003_project_updates'),
    ]

    operations = [
        migrations.CreateModel(
            name='TechnicalDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_description', models.CharField(blank=True, max_length=255)),
                ('document', models.FileField(upload_to='documents/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
