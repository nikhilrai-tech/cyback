# Generated by Django 3.2.16 on 2024-04-26 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_report_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='external',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Managed By External'),
        ),
    ]
