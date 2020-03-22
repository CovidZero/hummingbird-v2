import json
from unittest import TestCase
from app import app, db
from models import City,CasesLocation
from tests.runner import clear_db


class TestDataApi(TestCase):

    def setUp(self):
        self.app_context = app.test_request_context()
        self.app_context.push()
        self.client = app.test_client()
        self.app = app
        db.create_all()
        self.db = db

    def tearDown(self):
        clear_db(self.db)

    def test_return_cases_by_state_without_reports(self):
        resp = self.client.get('/data_api/v1/data/state/SP')
        data = json.loads(resp.get_data(as_text=True))

        assert len(data) == 4

        assert 'activeCases' in data
        assert 'suspectedCases' in data
        assert 'recoveredCases' in data
        assert 'deaths' in data

        assert data['activeCases'] == 0
        assert data['suspectedCases'] == 0
        assert data['recoveredCases'] == 0
        assert data['deaths'] == 0

    def test_return_cases_by_state_with_reports(self):
        # Generate test data
        City().save(self.db.session, city='Igarapava', state='SP',
                    country='Brasil', total_cases=45, suspects=35, refuses=3, deaths=2, recovered=1)
        City().save(self.db.session, city='Franca', state='SP',
                    country='Brasil', total_cases=50, suspects=35, refuses=3, deaths=1, recovered=1)

        # Should not include this data
        City().save(self.db.session, city='Uberaba', state='MG',
                    country='Brasil', total_cases=50, suspects=35, refuses=3, deaths=1, recovered=1)
        self.db.session.commit()

        resp = self.client.get('/data_api/v1/data/state/SP')
        data = json.loads(resp.get_data(as_text=True))

        assert len(data) == 4

        assert 'activeCases' in data
        assert 'suspectedCases' in data
        assert 'recoveredCases' in data
        assert 'deaths' in data

        assert data['activeCases'] == 14
        assert data['suspectedCases'] == 70
        assert data['recoveredCases'] == 2
        assert data['deaths'] == 3

    def test_return_all_cases(self):
        #generate test data
        City().save(self.db.session, city="c1", state="s1", country="c1", total_cases=20, suspects=5, refuses=3, deaths=2, recovered=1)

        City().save(self.db.session, city="c2", state="s2", country="c1", total_cases=20, suspects=5, refuses=3, deaths=2, recovered=1)

        self.db.session.commit()

        #act
        resp = self.client.get('/data_api/v1/data/all')
        data = json.loads(resp.get_data(as_text=True))

        #assert
        assert len(data) == 4
        
        assert 'activeCases' in data
        assert 'suspectedCases' in data
        assert 'recoveredCases' in data
        assert 'deaths' in data

        assert data['activeCases'] == 18
        assert data['suspectedCases'] == 10
        assert data['recoveredCases'] == 2
        assert data['deaths'] == 4

    def test_return_cases_by_search_city(self):
        #generate test data
        City().save(self.db.session, city="c1", state="s1", country="c1", total_cases=20, suspects=5, refuses=3, deaths=2, recovered=1)

        City().save(self.db.session, city="c2", state="s2", country="c1", total_cases=20, suspects=5, refuses=3, deaths=2, recovered=1)

        self.db.session.commit()

        #act
        resp = self.client.get('/data_api/v1/data/search?query=c1')
        data = json.loads(resp.get_data())

        city_data1 = data[0]

        #assert
        assert len(data) == 1
        assert city_data1['city'] == "c1"
        assert city_data1['state'] == "s1"
        assert city_data1['cases']['activeCases'] == 9
        assert city_data1['cases']['suspectedCases'] == 5
        assert city_data1['cases']['recoveredCases'] == 1
        assert city_data1['cases']['deaths'] == 2

    def test_return_cases_by_search_state(self):
        #generate test data
        City().save(self.db.session, city="c1", state="s1", country="c1", total_cases=20, suspects=5, refuses=3, deaths=2, recovered=1)

        City().save(self.db.session, city="c2", state="s2", country="c1", total_cases=20, suspects=5, refuses=3, deaths=2, recovered=1)

        self.db.session.commit()

        #act
        resp = self.client.get('/data_api/v1/data/search?query=s2')
        data = json.loads(resp.get_data())

        city_data1 = data[0]

        #assert
        assert len(data) == 1
        assert city_data1['city'] == "c2"
        assert city_data1['state'] == "s2"
        assert city_data1['cases']['activeCases'] == 9
        assert city_data1['cases']['suspectedCases'] == 5
        assert city_data1['cases']['recoveredCases'] == 1
        assert city_data1['cases']['deaths'] == 2

    def test_return_cases_by_search_multiple_cities(self):
        #generate test data
        City().save(self.db.session, city="c1", state="s1", country="c1", total_cases=20, suspects=5, refuses=3, deaths=2, recovered=1)

        City().save(self.db.session, city="c2", state="s2", country="c1", total_cases=20, suspects=5, refuses=3, deaths=2, recovered=1)
        City().save(self.db.session, city="c3", state="s2", country="c1", total_cases=20, suspects=5, refuses=3, deaths=2, recovered=1)

        self.db.session.commit()

        #act
        resp = self.client.get('/data_api/v1/data/search?query=s2')
        data = json.loads(resp.get_data())

        city_data1 = data[0]
        city_data2 = data[1]

        #assert
        assert len(data) == 2
        assert city_data1['city'] == "c2"
        assert city_data1['state'] == "s2"
        assert city_data1['cases']['activeCases'] == 9
        assert city_data1['cases']['suspectedCases'] == 5
        assert city_data1['cases']['recoveredCases'] == 1
        assert city_data1['cases']['deaths'] == 2

        assert city_data2['city'] == "c3"
        assert city_data2['state'] == "s2"
        assert city_data2['cases']['activeCases'] == 9
        assert city_data2['cases']['suspectedCases'] == 5
        assert city_data2['cases']['recoveredCases'] == 1
        assert city_data2['cases']['deaths'] == 2

    #Obter um array de casos de COVID-19 próximos ao usuário
    # /[nome_a_definir]?lat=[LATITUDE]&lng=[LONGITUDE]
    def test_return_cases_near_user(self):
        # Generate test data
        CasesLocation().save(self.db.session, id=0, city='Porto Alegre', state='RS',
                    country='Brasil', status='ACTIVE', latitude=-29.974343, longitude=-51.195532)
        CasesLocation().save(self.db.session, id=1, city='Porto Alegre', state='RS',
                    country='Brasil', status='SUSPECTED', latitude=-29.974343, longitude=-51.195532)
        CasesLocation().save(self.db.session, id=2, city='Porto Alegre', state='RS',
                    country='Brasil', status='RECOVERED', latitude=-29.974343, longitude=-51.195532)

        # Should not include this data
        CasesLocation().save(self.db.session, id=3, city='Igarapava', state='SP',
                    country='Brasil', status='RECOVERED', latitude=-20.047582, longitude=-47.780110)
        self.db.session.commit()

        resp = self.client.get('/data_api/v1/data/cases_location?lat=-29.974343&lng=-51.195532')
        data = json.loads(resp.get_data(as_text=True))
        print("response:",data)




