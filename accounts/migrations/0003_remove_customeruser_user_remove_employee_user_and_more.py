# Generated by Django 4.2.5 on 2023-09-26 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_customeruser_user_alter_employee_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customeruser',
            name='user',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='user',
        ),
        migrations.RemoveField(
            model_name='user',
            name='uid',
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[(1, 'User'), (2, 'ClientUser')], default=1, max_length=10),
        ),
        migrations.DeleteModel(
            name='AdminHOD',
        ),
        migrations.DeleteModel(
            name='CustomerUser',
        ),
        migrations.DeleteModel(
            name='Employee',
        ),
    ]
