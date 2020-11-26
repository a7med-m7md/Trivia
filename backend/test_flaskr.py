import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgres://{}@{}/{}".format('postgres:242512','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'Which four states make up the 4 Corners region of the US?',
            'answer': 'Colorado, New Mexico, Arizona, Utah',
            'difficulty': 3,
            'category': 'Science'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_getCategories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertNotEqual(len(data['categories']),0)

    
    def test_get_paginated_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data['questions']))

    def test_404_request_beyond_valid_page(self):
        response = self.client().get('/questions?page=100')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)

    def test_delete_question(self):
        question = Question(question=self.new_question['question'], answer=self.new_question['answer'],
                            category=self.new_question['category'], difficulty=self.new_question['difficulty'])
        question.insert()
        q_id = question.id
        questions_before = Question.query.all()
        response = self.client().delete('/questions/{}'.format(q_id))
        data = json.loads(response.data)
        questions_after = Question.query.all()
        question = Question.query.filter(Question.id == 1).one_or_none()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(question, None)

    def test_422_if_question_creation_fails(self):
        questions_before = Question.query.all()
        response = self.client().post('/questions', json={})
        data = json.loads(response.data)
        questions_after = Question.query.all()
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], "False")
        self.assertTrue(len(questions_after) == len(questions_before))


    def test_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)

    def test_search(self):
        res = self.client().post('/search',json={"searchTerm":"club"})
        data = json.loads(res.data)
        self.assertEqual(len(data['questions']),1)


    def test_404_if_search_questions_fails(self):
        response = self.client().post('/questions',
                                      json={'searchTerm': 'abcdefghijk'})
        data = json.loads(response.data)
        self.assertEqual(data['Success'], "False")
    def test_getByCategory(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(data['success'],'True')
     
    
    def test_400_if_questions_by_category_fails(self):
        response = self.client().get('/categories/100/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['Success'], 'False')
        self.assertEqual(data['Message'], 'Bad Request')


    def test_quizzes(self):
        res = self.client().post('/quizzes',json={'previous_questions': [20, 21],
                                            'quiz_category': {'type': 'Science', 'id': '1'}})
        self.assertEqual(res.status_code,200)

    def test_quiz_fails(self):
        response = self.client().post('/quizzes', json={})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['Success'], "False")

    def test_create_new_question(self):
        questions_before = Question.query.all()
        response = self.client().post('/questions', json=self.new_question)
        data = json.loads(response.data)
        questions_after = Question.query.all()
        self.assertEqual(data['success'], 'True')
        self.assertTrue(len(questions_after) - len(questions_before) == 1)

    def test_422_if_question_creation_fails(self):
        questions_before = Question.query.all()
        response = self.client().post('/questions', json={})
        data = json.loads(response.data)
        questions_after = Question.query.all()
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['Success'], "False")
        self.assertTrue(len(questions_after) == len(questions_before))



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()