from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("adds", "0005_message_is_read"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="image",
            field=models.ImageField(blank=True, max_length=500, null=True, upload_to="posts/"),
        ),
    ]
