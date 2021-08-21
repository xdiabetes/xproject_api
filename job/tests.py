import json

from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase

from job.models import Job
from user_profile.tests import create_superuser_user_profile, create_normal_user_profile


class JobsTests(APITestCase):

    def setUp(self) -> None:
        self.superuser = create_superuser_user_profile(phone_number='09017938091')
        self.normal_user = create_normal_user_profile(phone_number='09303131503')

        self.software_eng = Job.objects.create(title='software eng.')
        self.sample_jobs = [self.software_eng, ]

        for job_data in self.sample_jobs_data():
            self.sample_jobs.append(Job.objects.create(**job_data))

    def sample_jobs_data(self):
        return [
            {'title': 'Programmer', 'parent': self.software_eng},
            {'title': 'Driver', 'parent': None}
        ]

    def jobs_serialized(self):
        return [{
            'pk': job.pk,
            'title': job.title,
            'parent': job.parent.pk if job.parent else None
        } for job in self.sample_jobs]

    def do_login(self, user_profile):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + user_profile.token)

    def test_create_job_superuser_should_pass(self):
        self.do_login(self.superuser)
        endpoint = reverse('job:job_create')
        response = self.client.post(endpoint, data={'title': 'Programmer'})

        self.assertEqual(response.status_code, 201)

    def test_create_job_normal_user_should_fail(self):
        self.do_login(self.normal_user)
        endpoint = reverse('job:job_create')
        response = self.client.post(endpoint, data={'title': 'Programmer'})

        self.assertEqual(response.status_code, 403)

    def test_job_update(self):
        self.do_login(self.superuser)
        endpoint = reverse('job:job_update', kwargs={'job_id': self.software_eng.pk})

        response = self.client.patch(endpoint, data={'title': 'Software Engineer'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['title'], 'Software Engineer')

    def test_list_jobs(self):
        endpoint = reverse('job:job_list')

        response = self.client.get(endpoint)
        self.assertJSONEqual(response.content, json.dumps(self.jobs_serialized()))
        self.assertEqual(response.status_code, 200)