import unittest
from emissions import app, db, Country, EmissionData

class EmissionAppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app = app.test_client()

        with app.app_context():
            db.create_all()
            country = Country(name="Testland", code="TL", region="Nowhere", income_group="High income")
            db.session.add(country)
            db.session.commit()

            data = EmissionData(country_id=country.id, year=2020, emission=4.5)
            db.session.add(data)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_homepage(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Testland', response.data)

    def test_country_detail(self):
        with app.app_context():
            country = Country.query.filter_by(name="Testland").first()
            response = self.app.get(f'/country/{country.id}')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Testland', response.data)
            self.assertIn(b'TL', response.data)

    def test_404(self):
        response = self.app.get('/country/9999')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'The Page does not exist', response.data)

if __name__ == '__main__':
    unittest.main()
