# Generated by Django 3.0.8 on 2020-08-07 03:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0009_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='cate',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='pybo.Category'),
            preserve_default=False,
        ),
    ]
