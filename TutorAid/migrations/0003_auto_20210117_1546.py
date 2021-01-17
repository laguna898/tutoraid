# Generated by Django 3.0.5 on 2021-01-17 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TutorAid', '0002_auto_20210117_1545'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'managed': True},
        ),
        migrations.AddField(
            model_name='registration',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='TutorAid.Course'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registration',
            name='student',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='TutorAid.Student'),
            preserve_default=False,
        ),
    ]
