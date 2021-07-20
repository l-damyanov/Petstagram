# Generated by Django 3.2.5 on 2021-07-20 12:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, to='accounts.petstagramuser'),
            preserve_default=False,
        ),
    ]
