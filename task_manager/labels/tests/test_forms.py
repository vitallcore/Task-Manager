from task_manager.labels.forms import LabelCreationForm
from task_manager.labels.tests.testcase import LabelTestCase


class TestLabelCreationForm(LabelTestCase):
    def test_missing_fields(self):
        form = LabelCreationForm(data={
            'name': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_duplicate(self):
        form = LabelCreationForm(data={
            'name': self.label1.name
        })
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_valid_form(self):
        form = LabelCreationForm(data=self.valid_label_data)
        self.assertTrue(form.is_valid())
