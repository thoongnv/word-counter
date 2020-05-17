from tests.test_base import BaseTestCase
from utils.counter import WordCounter


class WordCounterTestCase(BaseTestCase):
    def test_frequency(self):
        counter = WordCounter.from_html("""
            <html>
                <body>
                    <p>
                        Hello world, hello there!
                    </p>
                    <p>
                        Hello world again!
                    </p>
                </body>
            </html>
        """)
        self.assertEqual(dict(counter), {
            'hello': 3,
            'world': 2,
            'there': 1,
            'again': 1
        })

    def test_normalize(self):
        counter = WordCounter.from_html("""
            <html>
                <body>
                    <p>
                        Canifa manage an e-shop and furniture&nbsp;stores throughout Vietnam.
                    </p>
                </body>
            </html>
        """)
        self.assertEqual(dict(counter), {
            'canifa': 1,
            'manage': 1,
            'an': 1,
            'e-shop': 1,
            'and': 1,
            'furniture': 1,
            'stores': 1,
            'throughout': 1,
            'vietnam': 1
        })

    def test_skip_tags(self):
        counter = WordCounter.from_html("""
            <html>
                <head>
                    <title>Trobz | Leading Odoo Integrator From Vietnam</title>
                    <script type="text/javascript">
                        var odoo = {
                            csrf_token: "757600ba3b55d72f27ebe45bb7beedd75518b0dco",
                        };
                    </script>
                </head>
                <body>
                    <div class="col-lg-12 s_title pt32" data-name="Title">
                        <h1 style="text-align: center; font-size: 62px;">
                            <b>We deliver Odoo solutions</b>
                        </h1>
                        <h1 style="text-align: center; font-size: 62px;">
                            <b>tailored to your business</b>
                        </h1>
                    </div>
                </body>
            </html>
        """)
        self.assertEqual(dict(counter), {
            'we': 1,
            'deliver': 1,
            'odoo': 1,
            'solutions': 1,
            'tailored': 1,
            'to': 1,
            'your': 1,
            'business': 1
        })
