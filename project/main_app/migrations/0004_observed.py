# Generated by Django 3.2.3 on 2022-02-24 11:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0003_auto_20210601_1333'),
    ]

    operations = [
        migrations.CreateModel(
            name='Observed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='observed', to='main_app.case')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='observed', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
