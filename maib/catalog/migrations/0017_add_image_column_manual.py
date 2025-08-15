from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0016_alter_carpet_code_alter_carpet_color_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE catalog_carpet ADD COLUMN image VARCHAR(500);",
            reverse_sql="ALTER TABLE catalog_carpet DROP COLUMN image;"
        ),
    ]
