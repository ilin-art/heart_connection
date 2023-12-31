# Generated by Django 4.2.2 on 2023-06-28 09:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.BooleanField(choices=[(True, 'Like'), (False, 'Dislike')], verbose_name='Оценка')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_ratings', to=settings.AUTH_USER_MODEL, verbose_name='Отправитель')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incoming_ratings', to=settings.AUTH_USER_MODEL, verbose_name='Получатель')),
            ],
            options={
                'verbose_name': 'Оценка',
                'verbose_name_plural': 'Оценки',
            },
        ),
    ]
