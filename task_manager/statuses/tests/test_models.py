from task_manager.statuses.models import Status
from task_manager.statuses.tests.testcase import StatusTestCase


class TestStatusModel(StatusTestCase):
    def test_status_creation(self):
        status = Status.objects.create(
            name=self.valid_status_data['name']
        )
        self.assertEqual(status.name, self.valid_status_data['name'])
        self.assertEqual(str(status), self.valid_status_data['name'])

    def test_duplicate_status_name(self):
        Status.objects.create(
            name=self.valid_status_data['name']
        )
        with self.assertRaises(Exception):
            Status.objects.create(
                name=self.valid_status_data['name']
            )
