from task_manager.statuses.forms import StatusCreationForm
from task_manager.statuses.tests.testcase import StatusTestCase


class TestStatusCreationForm(StatusTestCase):
    def test_missing_fields(self):
        form = StatusCreationForm(data={
            'name': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_duplicate(self):
        form = StatusCreationForm(data={
            'name': self.status1.name
        })
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_valid_form(self):
        form = StatusCreationForm(data=self.valid_status_data)
        self.assertTrue(form.is_valid())
