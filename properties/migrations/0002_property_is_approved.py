from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='is_approved',
            field=models.BooleanField(default=False, verbose_name='معتمد من الإدارة'),
        ),
    ]
