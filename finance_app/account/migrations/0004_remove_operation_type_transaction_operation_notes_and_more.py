# Generated by Django 4.2.3 on 2023-07-09 14:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_operation_type_transaction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operation',
            name='type_transaction',
        ),
        migrations.AddField(
            model_name='operation',
            name='notes',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='type',
            name='TypeTransaction',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='operation',
            name='date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='operation',
            name='price',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.DeleteModel(
            name='TypeTransaction',
        ),
    ]