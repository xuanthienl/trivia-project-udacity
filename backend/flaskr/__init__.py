import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

class NotFound(Exception):
    pass

def create_app(test_config=None):
    app = Flask(__name__)
    if test_config is not None:
        setup_db(app, test_config['database_path'])
    else:
        setup_db(app)
    CORS(app)

    """
    CORS Headers
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    GET all categories
    """
    @app.route("/categories", methods=["GET"])
    def list_categories():
        try:
            categories = Category.query.order_by(Category.id).all()
            categories = {category.id: category.type for category in categories}

            return jsonify(
                {
                    "success": True,
                    "categories": categories
                }
            )
        except Exception as e:
            print(e)
            abort(500)

    """
    GET all questions
    """
    @app.route("/questions", methods=["GET"])
    def list_questions():
        try:
            page = request.args.get("page", 1, type=int)
            per_page = QUESTIONS_PER_PAGE
            questions = Question.query.order_by(Question.id).paginate(page=page, per_page=per_page)
            current_questions = [question.format() for question in questions.items]

            categories = Category.query.order_by(Category.id).all()
            categories = {category.id: category.type for category in categories}

            return jsonify(
                {
                    "success": True,
                    "questions": current_questions,
                    "total_questions": questions.total,
                    "categories": categories,
                    "current_category": ""
                }
            )
        except Exception as e:
            print(e)
            abort(500)

    """
    POST delete question
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            if question is None:
                raise NotFound

            question.delete()

            return jsonify(
                {
                    "success": True
                }
            )
        except NotFound:
            print('Resource does not exist.')
            abort(404)
        except Exception as e:
            print(e)
            abort(500)

    """
    POST create question
    """
    @app.route("/questions", methods=["POST"])
    def create_question():
        body = request.get_json()

        try:
            question = Question(
                question=body.get("question", None),
                answer=body.get("answer", None),
                difficulty=body.get("difficulty", None),
                category=body.get("category", None)
            )
            question.insert()

            return jsonify(
                {
                    "success": True
                }
            )
        except Exception as e:
            print(e)
            abort(422)

    """
    GET questions based on a search term
    """
    @app.route("/questions/search", methods=["POST"])
    def search_questions():
        body = request.get_json()

        try:
            searchTerm = body.get("searchTerm", None)

            page = request.args.get("page", 1, type=int)
            per_page = QUESTIONS_PER_PAGE
            questions = Question.query.filter((Question.question.ilike(f"%{searchTerm}%"))).paginate(page=page, per_page=per_page)
            current_questions = [question.format() for question in questions.items]

            return jsonify(
                {
                    "success": True,
                    "questions": current_questions,
                    "total_questions": questions.total,
                    "current_category": ""
                }
            )
        except Exception as e:
            print(e)
            abort(422)

    """
    GET questions based on category
    """
    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def list_questions_by_category(category_id):
        try:
            category = Category.query.filter(Category.id == category_id).one_or_none()
            if category is None:
                raise NotFound

            page = request.args.get("page", 1, type=int)
            per_page = QUESTIONS_PER_PAGE
            questions = Question.query.filter(Question.category == category_id).order_by(Question.id).paginate(page=page, per_page=per_page)
            current_questions = [question.format() for question in questions.items]

            return jsonify(
                {
                    "success": True,
                    "questions": current_questions,
                    "total_questions": questions.total,
                    "current_category": category.type
                }
            )
        except NotFound:
            print('Resource does not exist.')
            abort(404)
        except Exception as e:
            print(e)
            abort(500)

    """
    GET questions to play the quiz
    """
    @app.route("/quizzes", methods=["POST"])
    def quizzes():
        body = request.get_json()

        try:
            quiz_category = body.get("quiz_category", None)
            previous_questions = body.get("previous_questions", [])

            if quiz_category is None or quiz_category['id'] == 0:
                question = Question.query.filter(Question.id.notin_(previous_questions)).first()
            else:
                question = Question.query.filter(Question.category == quiz_category['id'], Question.id.notin_(previous_questions)).first()

            response = {
                "success": True,
            }
            if question is not None:
                response["question"] = question.format()

            return jsonify(response)
        except Exception as e:
            print(e)
            abort(422)

    """
    ERRORS handlers
    """
    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 400, "message": "Bad Request"}),
            400
        )

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "Not Found"}),
            404
        )

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return (
            jsonify({"success": False, "error": 422, "message": "Unprocessable Entity"}),
            422
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify({"success": False, "error": 405, "message": "Method Not Allowed"}),
            405
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify({"success": False, "error": 500, "message": "Internal Server Error"}),
            500
        )

    return app
