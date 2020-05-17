from tests.test_base import BaseTestCase


class StatisticTestCase(BaseTestCase):
    def test_get_statistic(self):
        # get unknown ID
        resp = self.client.get('/v1/statistics/-9999')
        self.assertEqual(resp.status_code, 404)

        # statistic example.com
        resp = self.client.post('/v1/statistics', json={
            'website_url': 'http://example.com',
        })
        self.assertEqual(resp.status_code, 201)

        # get previous statistic
        resp = self.client.get(
            '/v1/statistics/{}?order=-frequency&offset=2&limit=3'.format(
                resp.json['id']))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['url'], 'http://example.com')
        self.assertEqual(resp.json['words'], {
            'total': 21,
            'offset': 2,
            'limit': 3,
            'data': [
                {'id': 3, 'name': 'this', 'frequency': 2, 'site_id': 1},
                {'id': 5, 'name': 'for', 'frequency': 2, 'site_id': 1},
                {'id': 6, 'name': 'use', 'frequency': 2, 'site_id': 1},
            ]
        })

        # get all statistics
        resp = self.client.get('/v1/statistics?order=+frequency')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['total'], 1)
        self.assertEqual(resp.json['data'][0]['words'], {
            'total': 21,
            'offset': 0,
            'limit': 10,
            'data': [
                {'id': 1, 'name': 'example', 'frequency': 1, 'site_id': 1},
                {'id': 4, 'name': 'is', 'frequency': 1, 'site_id': 1},
                {'id': 8, 'name': 'illustrative', 'frequency': 1, 'site_id': 1},
                {'id': 9, 'name': 'examples', 'frequency': 1, 'site_id': 1},
                {'id': 10, 'name': 'documents', 'frequency': 1, 'site_id': 1},
                {'id': 11, 'name': 'you', 'frequency': 1, 'site_id': 1},
                {'id': 12, 'name': 'may', 'frequency': 1, 'site_id': 1},
                {'id': 13, 'name': 'literature', 'frequency': 1, 'site_id': 1},
                {'id': 14, 'name': 'without', 'frequency': 1, 'site_id': 1},
                {'id': 15, 'name': 'prior', 'frequency': 1, 'site_id': 1}
            ]
        })

    def test_create_statistic(self):
        # statistic fake website
        resp = self.client.post('/v1/statistics', json={
            'website_url': 'https://notexistingwebsite.com',
        })
        self.assertEqual(resp.status_code, 400)

        # statistic example.com
        resp = self.client.post('/v1/statistics', json={
            'website_url': 'http://example.com',
        })
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(resp.json['id'])
