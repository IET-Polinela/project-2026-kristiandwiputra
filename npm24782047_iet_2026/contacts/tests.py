from django.test import TestCase
from django.urls import reverse


class ContactsPageTests(TestCase):
    def test_contacts_page_is_accessible(self):
        response = self.client.get(reverse('contacts'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contacts/contacts.html')
