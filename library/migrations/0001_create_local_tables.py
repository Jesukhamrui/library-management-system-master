from django.db import migrations


class Migration(migrations.Migration):
	"""No-op initial migration for the legacy `library` app.

	The project's models were generated with `inspectdb` and many are
	`managed = False`. Providing an empty Migration class here prevents
	Django from raising BadMigrationError while keeping the app's
	migration history consistent. If you later convert models to be
	managed, replace this with real operations or create new migrations.
	"""

	initial = True
	dependencies = []
	operations = []

