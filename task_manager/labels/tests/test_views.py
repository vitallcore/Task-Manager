from django.urls import reverse_lazy

from task_manager.labels.models import Label
from task_manager.labels.tests.testcase import LabelTestCase


class TestLabelListView(LabelTestCase):
    def test_labels_list_authorized(self):
        user1 = self.user1
        self.client.force_login(user1)

        response = self.client.get(reverse_lazy('label_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/label_list.html')
        self.assertEqual(Label.objects.count(), self.label_count)

    def test_labels_list_unauthorized(self):
        response = self.client.get(reverse_lazy('label_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))


class TestLabelCreateView(LabelTestCase):
    def test_label_creation_authorized(self):
        user1 = self.user1
        self.client.force_login(user1)
        creation_data = self.valid_label_data
        initial_count = Label.objects.count()

        response = self.client.get(reverse_lazy('label_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

        response = self.client.post(
            reverse_lazy('label_create'), data=creation_data
        )
        self.assertEqual(Label.objects.count(), initial_count + 1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('label_list'))

    def test_label_creation_unauthorized(self):
        creation_data = self.valid_label_data

        response = self.client.get(reverse_lazy('label_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        response = self.client.post(
            reverse_lazy('label_create'), data=creation_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))


class TestLabelDeleteView(LabelTestCase):
    def test_label_deletion_unauthorized(self):
        label = self.label1

        response = self.client.get(
            reverse_lazy('label_delete', kwargs={'pk': label.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        response = self.client.post(
            reverse_lazy('label_delete', kwargs={'pk': label.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_label_deletion_authorized(self):
        user = self.user1
        label = self.label1
        self.client.force_login(user)
        initial_count = Label.objects.count()

        response = self.client.get(
            reverse_lazy('label_delete', kwargs={'pk': label.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'labels/label_delete.html')

        response = self.client.post(
            reverse_lazy('label_delete', kwargs={'pk': label.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('label_list'))
        self.assertEqual(Label.objects.count(), initial_count - 1)
        with self.assertRaises(Label.DoesNotExist):
            Label.objects.get(id=label.id)


class TestLabelUpdateView(LabelTestCase):
    def test_label_update_unauthorized(self):
        label = self.label1

        response = self.client.get(
            reverse_lazy('label_update', kwargs={'pk': label.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        response = self.client.post(
            reverse_lazy('label_update', kwargs={'pk': label.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_label_update_authorized(self):
        user = self.user1
        label = self.label1
        self.client.force_login(user)
        update_data = {'name': 'new'}

        response = self.client.get(
            reverse_lazy('label_update', kwargs={'pk': label.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')

        response = self.client.post(
            reverse_lazy('label_update', kwargs={'pk': label.id}),
            data=update_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('label_list'))
        updated_label = Label.objects.get(id=label.id)
        self.assertEqual(updated_label.name, update_data['name'])
