from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [("adds", "0004_message")]
    operations = [migrations.AddField(model_name="message", name="is_read", field=models.BooleanField(default=False))]
