# Generated by Django 3.1 on 2020-08-12 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0003_auto_20200812_1828'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='group_code',
            field=models.CharField(default='abc', max_length=100),
            preserve_default=False,
        ),
    ]
