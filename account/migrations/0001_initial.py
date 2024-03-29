# Generated by Django 4.2 on 2023-06-02 12:25

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cinema', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('television', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('country', models.CharField(max_length=50)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pictures')),
                ('birthday', models.DateField(blank=True, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?[\\d\\s-]+$')])),
                ('bio', models.TextField(blank=True)),
                ('vip_status', models.BooleanField(default=False)),
                ('vip_expiration', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteTVShow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tvshow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tvfavs', to='television.tvshow')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_tvfavs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteMovie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mfavs', to='cinema.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_mfavs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
