# Generated by Django 2.1.5 on 2021-05-09 23:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('management', '0001_initial'),
        ('ivr', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Helper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('helper_number', models.CharField(blank=True, max_length=16, null=True)),
                ('is_anonymous', models.BooleanField(default=True, help_text='tells whether helper number is anonymous')),
                ('gender', models.CharField(blank=True, max_length=16, null=True)),
                ('college_name', models.CharField(blank=True, max_length=256, null=True)),
                ('gcm_canonical_id', models.CharField(blank=True, max_length=256, null=True)),
                ('level', models.IntegerField(choices=[(1, 'PRIMARY'), (2, 'SECONDARY')], default=1)),
                ('helper_type', models.IntegerField(choices=[(1, 'DIRECT'), (2, 'INDIRECT')], default=2)),
                ('rating', models.DecimalField(decimal_places=2, default=2.5, max_digits=3)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created Timestamp')),
                ('last_assigned', models.DateTimeField(auto_now_add=True, verbose_name='Last Assigned Timestamp')),
                ('status', models.IntegerField(choices=[(1, 'Active'), (2, 'Blocked')], default=1)),
                ('login_status', models.IntegerField(choices=[(1, 'LOGGED_IN'), (2, 'LOGGED_OUT'), (3, 'PENDING')], default=3)),
                ('login_prevstatus', models.IntegerField(choices=[(1, 'LOGGED_IN'), (2, 'LOGGED_OUT'), (3, 'PENDING')], default=3)),
                ('category', models.ManyToManyField(blank=True, to='management.HelperCategory')),
                ('helpline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.HelpLine')),
                ('language', models.ManyToManyField(blank=True, to='ivr.Language')),
                ('subcategory', models.ManyToManyField(blank=True, to='management.CategorySubcategory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
