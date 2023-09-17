import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from flaskr import create_app
from models import setup_db, Question, Category

load_dotenv()

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.database_path = "{}://{}:{}@{}:{}/{}".format(
            os.getenv("DB_CONNECTION"),
            os.getenv("DB_USERNAME"),
            os.getenv("DB_PASSWORD"),
            os.getenv("DB_HOST"),
            os.getenv("DB_PORT"),
            os.getenv("DB_TEST_DATABASE")
        )
        test_config = {}
        test_config["database_path"] = self.database_path
        self.app = create_app(test_config)
        self.client = self.app.test_client

        # self.app = create_app()
        # self.client = self.app.test_client
        # self.database_name = "trivia_test"
        # self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        # setup_db(self.app, self.database_path)

        # # binds the app to the current context
        # with self.app.app_context():
        #     self.db = SQLAlchemy()
        #     self.db.init_app(self.app)
        #     # create all tables
        #     self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_list_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])

    def test_get_list_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertEqual(len(data["questions"]), 10)
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])
        self.assertEqual(data["current_category"], '')

    def test_delete_question(self):
        with self.app.app_context():
            question = Question.query.first()
            question_id = question.id

        with self.app.app_context():
            question = Question.query.filter(Question.id == question_id).one_or_none()
            self.assertNotEqual(question, None)

        res = self.client().delete("/questions/" + str(question_id))
        data = json.loads(res.data)

        with self.app.app_context():
            question = Question.query.filter(Question.id == question_id).one_or_none()
            self.assertEqual(question, None)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_404_for_delete_question(self):
        question_id = 1

        res = self.client().delete("/questions/" + str(question_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "Not Found")

    def test_create_question(self):
        new_question = {
            "question": "Is 1 plus 1 equal to 2?",
            "answer": "Yes",
            "difficulty": 1,
            "category": 5
        }
        res = self.client().post("/questions", json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_422_for_create_question(self):
        new_question = {
            "question": "Is 10 plus 10 equal to 2?",
            "answer": "No",
            "difficulty": 'Easy',
            "category": 5
        }
        res = self.client().post("/questions", json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 422)
        self.assertEqual(data["message"], "Unprocessable Entity")

    def test_search_questions(self):
        search_term = {
            "searchTerm": "1 plus 1"
        }
        res = self.client().post("/questions/search", json=search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertGreaterEqual(len(data["questions"]), 1)
        self.assertGreaterEqual(data["total_questions"], 1)
        self.assertEqual(data["current_category"], '')

    def test_search_questions_no_results(self):
        search_term = {
            "searchTerm": "10 plus 10"
        }
        res = self.client().post("/questions/search", json=search_term)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["questions"], [])
        self.assertEqual(data["total_questions"], 0)
        self.assertEqual(data["current_category"], '')

    def test_get_list_questions_by_category(self):
        res = self.client().get("/categories/5/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertLessEqual(len(data["questions"]), 10)
        self.assertTrue(data["total_questions"])
        self.assertEqual(data["current_category"], 'Entertainment')

    def test_404_for_get_list_questions_by_category(self):
        res = self.client().get("/categories/50/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "Not Found")

    def test_get_quizzes(self):
        previous_questions = []
        with self.app.app_context():
            question = Question.query.filter(Question.category == '5').first()
            if question is not None:
                previous_questions.append(question.id)

        req = {
            "quiz_category": {"type": 'Entertainment', "id": 5},
            "previous_questions": previous_questions
        }
        res = self.client().post("/quizzes", json=req)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])
        self.assertEqual(data["question"]['category'], req['quiz_category']['id'])
        if len(req['previous_questions']) > 0:
            self.assertNotEqual(data["question"]['id'], req['previous_questions'][0])

    def test_422_for_get_quizzes(self):
        req = {
            "quiz_category": 5,
            "previous_questions": []
        }
        res = self.client().post("/quizzes", json=req)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 422)
        self.assertEqual(data["message"], "Unprocessable Entity")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
