import os
import unittest
import json

from flaskr import create_app
from models import db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "trivia_test"
        self.database_user = "postgres"
        self.database_password = "Alona1996l!"
        self.database_host = "localhost:5432"
        self.database_path = f"postgresql://{self.database_user}:{self.database_password}@{self.database_host}/{self.database_name}"

        # Create app with the test configuration
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "TESTING": True
        })
        self.client = self.app.test_client()

        # Bind the app to the current context and create all tables
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            db.session.remove()
            # db.drop_all()

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # Get Categories tests
    def test_get_categories(self):
        # get response from endpoint
        res = self.client.get('/categories')

        # get data from response
        data = json.loads(res.data)

        # run assert statement to confirm expected result
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']), 6)

    def test_get_category_wrong_route_404(self):
        # get response from endpoint
        res = self.client.get('/category')

        # get data from response
        data = json.loads(res.data)

        # run assert statement to confirm expected result
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')


    # Get questions tests
    def test_get_paginated_questions(self):
        # get response from endpoint
        res = self.client.get('/questions?page=1')

        # get data from response
        data = json.loads(res.data)

        # run assert statement to confirm expected result
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']), 10)
        self.assertTrue(data['categories'], True)

    def test_get_questions_beyond_valid_page_404(self):
        # get response from endpoint
        res = self.client.get('/questions?page=500')

        # get data from response
        data = json.loads(res.data)

        # run assert statement to confirm expected result
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # Delete question tests
    def test_delete_question(self):
        # get response from endpoint
        res = self.client.delete('/questions/12')

        # get data from response
        data = json.loads(res.data)

        # run assert statement to confirm expected result
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']) > 0)

    def test_delete_question_not_exist_422(self):
        # get response from endpoint
        res = self.client.delete('/questions/5000')

        # get data from response
        data = json.loads(res.data)

        # run assert statement to confirm expected result
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Request contains invalid data')

    # Create question tests
    def test_create_question(self):
        # get response from endpoint
        res = self.client.post('/questions', json={'question': 'Test question', 
                                                   'answer': 'Test answer',
                                                   'difficulty': 1,
                                                   'category': '3'})

        # get data from response
        data = json.loads(res.data)

        # run assert statement to confirm expected result
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_question_no_data_422(self):
        # get response from endpoint
        res = self.client.post('/questions', json={'question': None})

        # get data from response
        data = json.loads(res.data)

        # run assert statement to confirm expected result
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Request contains invalid data')

    # Search questions tests
    def test_search_questions_with_results(self):
        # get response from endpoint
        res = self.client.post('/questions', json={'searchTerm': 'a'})

        # get data from response
        data = json.loads(res.data)

        # run assert statement to confirm expected result
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['totalQuestions'] > 0)


    def test_search_questions_no_results(self):
        # get response from endpoint
        res = self.client.post('/questions', json={'searchTerm': 'zzz'})

        # get data from response
        data = json.loads(res.data)

        # run assert statement to confirm expected result
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['totalQuestions'] == 0)

    # Get questions in category tests
    def test_get_questions_in_category(self):
        # get response from endpoint
        res = self.client.get('/categories/1/questions')

        # get data from response
        data = json.loads(res.data)

        # run assert statement to confirm expected result
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['totalQuestions'] > 0)
        self.assertEqual(data['currentCategory'], 'Science')

    def test_get_questions_in_category(self):
        # get response from endpoint
        res = self.client.get('/categories/100/questions')

        # get data from response
        data = json.loads(res.data)

        # run assert statement to confirm expected result
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # Get quiz questions tests
    def test_get_quiz_questions(self):
        # get response from endpoint
        res = self.client.post('/quizzes', json={'previous_questions': [], 
                                                'quiz_category': {'id': 1, 'type': 'Science'}})

        # get data from response
        data = json.loads(res.data)

        # run assert statement to confirm expected result
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['question']), 5)

    def test_get_quiz_questions_no_data_400(self):
        # get response from endpoint
        res = self.client.post('/quizzes')

        # get data from response
        data = json.loads(res.data)

        # run assert statement to confirm expected result
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

        



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
