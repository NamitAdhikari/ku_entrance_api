# Generated by Django 3.1.3 on 2020-11-22 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ku_entrance_api', '0009_questions_subject'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='question',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='subject',
        ),
        migrations.AddField(
            model_name='quiz',
            name='chem_question',
            field=models.ManyToManyField(blank=True, related_name='chem', to='ku_entrance_api.Questions'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='math_question',
            field=models.ManyToManyField(blank=True, related_name='math', to='ku_entrance_api.Questions'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='phys_question',
            field=models.ManyToManyField(blank=True, related_name='phys', to='ku_entrance_api.Questions'),
        ),
    ]