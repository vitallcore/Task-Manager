from task_manager.labels.models import Label
from task_manager.labels.tests.testcase import LabelTestCase


class TestLabelModel(LabelTestCase):
    def test_label_creation(self):
        label = Label.objects.create(
            name=self.valid_label_data['name']
        )
        self.assertEqual(label.name, self.valid_label_data['name'])
        self.assertEqual(str(label), self.valid_label_data['name'])

    def test_duplicate_label_name(self):
        Label.objects.create(
            name=self.valid_label_data['name']
        )
        with self.assertRaises(Exception):
            Label.objects.create(
                name=self.valid_label_data['name']
            )
