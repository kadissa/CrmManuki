# Generated by Django 5.0.2 on 2024-03-24 23:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webhooks', '0006_alter_customer_end_alter_customer_start_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Customer',
            new_name='Guest',
        ),
    ]
