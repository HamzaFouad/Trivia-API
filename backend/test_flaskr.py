import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

OK = 200
CREATED = 201
BAD_REQUEST = 400
NOT_FOUND = 404
NOT_PROCESSABLE = 422

class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('', self.database_name) # 'localhost:5432'
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, OK)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))


    def test_get_page_of_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, OK)
        self.assertEqual(data['success'], True)
        # it is okay to have no questions
        # self.assertTrue(len(data['page_of_questions']))
        # self.assertTrue(data['total_questions']) # total_questions = len of questions
        # self.assertTrue(len(data['page_of_questions']))


    def test_success_delete_question(self):
        deleted_test_id = 5
        res = self.client().delete(f'/questions/{deleted_test_id}')
        data = json.loads(res.data)
        
        question = Question.query.get(deleted_test_id)

        self.assertEqual(res.status_code, OK)
        self.assertEqual(data['success'], True)
        self.assertEqual(question, None) # check if truely deleted!
        self.assertEqual(data['deleted'], deleted_test_id)


    def test_delete_not_existing_question(self):
        deleted_test_id = 1000
        res = self.client().delete(f'/questions/{deleted_test_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, NOT_FOUND)
        self.assertEqual(data['error'], NOT_FOUND)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "RESOURCE NOT FOUND")


    def test_success_create_question(self):
        res = self.client().post('/questions', json={
                                                    'question': 'Question?',
                                                    'answer': 'Answered!',
                                                    'difficulty': 1,
                                                    'category': 1
                                                })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, CREATED)
        self.assertEqual(data['success'], True)
    

    def test_create_question_with_missing_parameters(self):
        '''
            missing parameter when creating question. --> BAD REQUEST
        '''
        res = self.client().post('/questions', json={
                                                    'question': 'Question?',
                                                    'answer': None, # Intended missed value --> should raise exception
                                                    'difficulty': 1,
                                                    'category': 1
                                                })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, BAD_REQUEST)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "BAD REQUEST")
    

    def test_search_not_existing_question(self):
        search_term = "Non-existing-search-term"
        res = self.client().post('/questions', json={"searchTerm": search_term})
        data = json.loads(res.data)

        # no need for exception when you don't find the search-term
        question = Question.query.filter(
          Question.question.ilike(f'%{search_term}%')
          ).all()

        self.assertFalse(len(question)) # len(question) = 0
        self.assertEqual(data['success'], True)
        

    def test_success_get_questions_by_existing_category(self):
        category_id = 1
        res = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, OK)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertNotEqual(data['current_category'], None) 


    def test_get_questions_by_non_existing_category(self):
        category_id = 1000
        res = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(res.data)

        # no need for exception when you don't find any questions in that category!
        self.assertEqual(res.status_code, BAD_REQUEST)
        self.assertEqual(data['success'], False)

    
    def test_success_quiz(self):
        previous_ids = [10, 11, 12]
        res = self.client().post('/quizzes', json={
            'previous_questions': previous_ids,
            'quiz_category': {'id':1, 'type':"Science"}
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, OK)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['category'], 1)
        self.assertTrue(data["question"]["id"] not in previous_ids)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()