# Generated by Django 4.2.5 on 2023-10-05 11:31

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0004_alter_invoice_invoice_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='invoice_id',
            field=models.UUIDField(default=uuid.UUID('70c1d6d7-dc52-44cf-981f-e1756dca5b5a'), editable=False, primary_key=True, serialize=False),
        ),
    ]