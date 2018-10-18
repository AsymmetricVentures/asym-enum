from django.core.management import call_command
from django.test.runner import DiscoverRunner

try:
	from django.contrib.auth import get_user_model
except ImportError:
	USERNAME_FIELD = 'username'
else:
	USERNAME_FIELD = get_user_model().USERNAME_FIELD

class TestRunner(DiscoverRunner):
	def setup_databases(self, *args, **kwargs):
		result = super(TestRunner, self).setup_databases(*args, **kwargs)
		kwargs = {
			'interactive': False,
			'email': 'admin@example.com',
			USERNAME_FIELD: 'admin'
		}
		call_command('createsuperuser', **kwargs)
		return result
	
	def build_suite(self, *args, **kwargs):
		suite = super(TestRunner, self).build_suite(*args, **kwargs)
		tests = []
		for case in suite:
			pkg = case.__class__.__module__
			if not pkg.startswith('django'):
				tests.append(case)
		suite._tests = tests
		return suite