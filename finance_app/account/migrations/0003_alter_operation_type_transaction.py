# Generated by Django 4.2.3 on 2023-07-07 22:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_typetransaction_alter_operation_account_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation',
            name='type_transaction',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.PROTECT, related_name='type_transaction', to='account.typetransaction'),
        ),
    ]