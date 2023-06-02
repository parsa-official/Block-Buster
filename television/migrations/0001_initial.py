# Generated by Django 4.2 on 2023-06-02 12:25

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cinema', '0001_initial'),
        ('people', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character_name', models.CharField(max_length=255)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='television_casts', to='people.person')),
            ],
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TVShow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('slug', models.SlugField(blank=True, max_length=255, null=True)),
                ('release_year', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2023)])),
                ('finish_year', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2023)])),
                ('imdb_id', models.CharField(blank=True, max_length=9, null=True, unique=True)),
                ('mpaa_rating', models.CharField(blank=True, choices=[('TV-Y', 'Suitable for all Children'), ('TV-Y7', 'Suitable for Children aged 7 and up'), ('TV-G', 'Suitable for all ages)'), ('TV-PG', 'Parental Guidance Suggested'), ('TV-14', 'Parents Strongly Cautioned'), ('TV-MA', 'Mature Audiences Only')], max_length=5, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='tvshow_images')),
                ('rating', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(10.0)])),
                ('runtime', models.PositiveIntegerField(blank=True, null=True)),
                ('synopsis', models.TextField(blank=True, null=True)),
                ('is_on_slideshow', models.BooleanField(default=False)),
                ('num_seasons', models.PositiveIntegerField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('now playing', 'Now Playing'), ('ended', 'Ended')], max_length=50)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=746, multiple=True)),
                ('cast', models.ManyToManyField(blank=True, related_name='movies', to='television.cast')),
                ('genres', models.ManyToManyField(blank=True, to='cinema.genre')),
                ('network', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='television.network')),
                ('plot_keywords', models.ManyToManyField(blank=True, to='cinema.plotkeyword')),
                ('writers', models.ManyToManyField(blank=True, related_name='written_tvshow', to='people.person')),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season_number', models.PositiveIntegerField()),
                ('image', models.ImageField(upload_to='season_images')),
                ('episode_number', models.PositiveIntegerField()),
                ('tv_show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seasons', to='television.tvshow')),
            ],
            options={
                'ordering': ['tv_show__title', 'season_number'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(max_length=400)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('liked_users', models.ManyToManyField(blank=True, related_name='series_liked_comments', to=settings.AUTH_USER_MODEL)),
                ('tvshow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='series_mcomments', to='television.tvshow')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='series_ucomments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='cast',
            name='tvshow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='casts', to='television.tvshow'),
        ),
    ]
