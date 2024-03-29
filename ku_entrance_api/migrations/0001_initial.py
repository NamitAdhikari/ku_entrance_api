# Generated by Django 3.1.3 on 2020-11-23 18:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PayVerificationCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('is_active', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
        ),
        migrations.CreateModel(
            name='QstnSubject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(blank=True, null=True)),
                ('level', models.IntegerField(default=1)),
                ('option1', models.TextField(blank=True, null=True)),
                ('option2', models.TextField(blank=True, null=True)),
                ('option3', models.TextField(blank=True, null=True)),
                ('option4', models.TextField(blank=True, null=True)),
                ('answer', models.CharField(blank=True, choices=[('a', models.TextField(blank=True, null=True)), ('b', models.TextField(blank=True, null=True)), ('c', models.TextField(blank=True, null=True)), ('d', models.TextField(blank=True, null=True))], max_length=2, null=True)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ku_entrance_api.qstnsubject')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quiz_name', models.CharField(max_length=75)),
                ('score', models.IntegerField(default=0)),
                ('activation_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pay_code', to='ku_entrance_api.payverificationcode')),
                ('chem_question', models.ManyToManyField(blank=True, related_name='chem', to='ku_entrance_api.Questions')),
                ('math_question', models.ManyToManyField(blank=True, related_name='math', to='ku_entrance_api.Questions')),
                ('phys_question', models.ManyToManyField(blank=True, related_name='phys', to='ku_entrance_api.Questions')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
