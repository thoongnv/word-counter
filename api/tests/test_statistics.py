from tests.test_base import BaseTestCase


class StatisticTestCase(BaseTestCase):
    def test_create_statistic(self):
        # statistic fake website
        resp = self.client.post('/v1/statistics', json={
            'website_url': 'https://notexistingwebsite.com',
        })
        self.assertEqual(resp.status_code, 400)

        # statistic google.com
        resp = self.client.post('/v1/statistics', json={
            'website_url': 'https://google.com',
        })
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(resp.json['id'])
