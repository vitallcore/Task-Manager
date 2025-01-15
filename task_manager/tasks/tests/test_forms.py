from task_manager.tasks.forms import TaskCreationForm
from task_manager.tasks.tests.testcase import TaskTestCase


class TestTaskCreationForm(TaskTestCase):
    def test_valid_data(self):
        author = self.user1
        form = TaskCreationForm(data=self.valid_task_data)
        self.assertTrue(form.is_valid())
        task = form.save(commit=False)
        task.author = author
        task.save()

    def test_empty_strings(self):
        invalid_data = self.valid_task_data.copy()
        invalid_data.update({
            'name': '',
            'description': ''
        })
        form = TaskCreationForm(invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('description', form.errors)

    def test_duplicate_task_name(self):
        author = self.user1
        form1 = TaskCreationForm(data=self.valid_task_data)
        task = form1.save(commit=False)
        task.author = author
        task.save()

        duplicate_data = self.valid_task_data.copy()
        duplicate_data.update({
            'description': 'New new description'
        })
        form2 = TaskCreationForm(data=duplicate_data)
        self.assertFalse(form2.is_valid())
        self.assertIn('name', form2.errors)
