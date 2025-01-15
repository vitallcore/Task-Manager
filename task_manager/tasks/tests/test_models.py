from task_manager.tasks.models import Task
from task_manager.tasks.tests.testcase import TaskTestCase


class TestTaskModel(TaskTestCase):
    def test_task_creation(self):
        task = Task.objects.create(
            name=self.valid_task_data['name'],
            description=self.valid_task_data['description'],
            status=self.status1,
            executor=self.user2,
            author=self.user1,
        )
        task.labels.set([self.label1, self.label2])
        self.assertEqual(task.name, self.valid_task_data['name'])
        self.assertEqual(task.description, self.valid_task_data['description'])
        self.assertEqual(task.author, self.user1)
        self.assertEqual(task.executor, self.user2)
        self.assertEqual(task.status, self.status1)
        self.assertCountEqual(list(task.labels.all()), [self.label1, self.label2])
        self.assertEqual(str(task), self.valid_task_data['name'])
