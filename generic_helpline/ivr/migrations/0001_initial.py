# Generated by Django 2.1.5 on 2021-05-09 23:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Call_Forward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('helper_no', models.CharField(max_length=15)),
                ('caller_no', models.CharField(max_length=15)),
                ('type', models.CharField(blank='True', choices=[('regular', 'regular'), ('survey', 'survey')], max_length=13, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Call_Forward_Details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('helper_no', models.CharField(max_length=15)),
                ('caller_no', models.CharField(max_length=15)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('initiated', 'initiated'), ('not_answered', 'not_answered'), ('completed', 'completed')], default='initiated', max_length=15)),
                ('call_duration', models.CharField(default='0', max_length=5)),
                ('call_pickup_duration', models.CharField(default='0', max_length=5)),
                ('call_recording', models.FileField(default='recordings/file.mp3', upload_to='recordings/')),
                ('call_recording_name', models.CharField(max_length=30, null=True)),
                ('type', models.CharField(blank='True', choices=[('regular', 'regular'), ('survey', 'survey')], max_length=13, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_question', models.IntegerField(default=0)),
                ('isCallRaised', models.BooleanField(default=False)),
                ('isFeedbackTaken', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='FeedbackResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.IntegerField(default=2)),
            ],
        ),
        migrations.CreateModel(
            name='FeedbackType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=100)),
                ('audio', models.FileField(upload_to='ivr_audio/')),
            ],
        ),
        migrations.CreateModel(
            name='IVR_Audio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio', models.FileField(upload_to='ivr_audio/')),
                ('playorder', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='IVR_Call',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sid', models.CharField(max_length=256)),
                ('caller_no', models.CharField(max_length=15)),
                ('caller_location', models.CharField(max_length=256)),
                ('helpline_no', models.CharField(max_length=15)),
                ('language_option', models.CharField(default=None, max_length=20, null=True)),
                ('category_option', models.CharField(default=None, max_length=20, null=True)),
                ('category_sub_option', models.CharField(default=None, max_length=20, null=True)),
                ('session_next', models.CharField(choices=[(0, 'welcome'), (1, 'display_language'), (2, 'get_language'), (3, 'display_option'), (4, 'get_option'), (5, 'display_sub_option'), (6, 'get_sub_option'), (7, 'display_terms'), (8, 'get_terms'), (9, 'call_exit'), (10, 'call_forward'), (11, 'call_direct'), (12, 'intro_1'), (13, 'get_intro_1_inp'), (14, 'intro_2'), (15, 'get_intro_2_inp'), (16, 'display_option_2'), (17, 'get_option_2')], max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Misc_Audio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio', models.FileField(upload_to='ivr_audio/')),
                ('playorder', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Misc_Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='misc_audio',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ivr.Misc_Category'),
        ),
    ]