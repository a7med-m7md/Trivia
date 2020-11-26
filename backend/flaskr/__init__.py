import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # mange all resources to access all the end points
    CORS(app, resources={r"/*": {"origins": "*"}})

    # handle the type of headers and accepted methods
    @app.after_request
    def after_request(response):
        header = 'Access-Control-Allow-'
        type_auth = 'Content-Type,Authorization'
        response.headers.add('{}Headers'.format(header), type_auth)
        response.headers.add('{}Methods'.format(header), '*')
        response.headers.add('{}Credentials'.format(header), 'true')
        return response

    # GET all the categories from my database
    #  and return it as JSON object
    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()
        if categories is not None:
            Category_ = {}
            for category in categories:
                Category_[category.id] = category.type
            return {
              "categories": Category_
              }, 200
        return abort(404)

    # get all the questions from my DB 
    # and return it as JSON object with the total questions number 
    @app.route('/questions', methods=['GET'])
    def getQuestions():
        page_no = request.args.get('page', type=int)
        questions = Question.query.paginate(page_no, QUESTIONS_PER_PAGE)
        questions_no = questions.total
        questions = [ques.format() for ques in questions.items]
        categories = [question["category"] for question in questions]
        return {
          "questions": questions,
          "total_questions": questions_no,
          "categories": categories,
          "currentCategory": get_categories()
        }

    # Delete a specific questions using its ID 
    # and return as JSON object succcess if it happens successfully
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        question = Question.query.filter_by(id=id).one_or_none()
        if question is not None:
            question.delete()
            return {
              "sucess": "true"
              }, 200
        return abort(405)

    # handling add questions by using post method 
    # and recieve all different informaions about this question
    @app.route('/questions', methods=["POST"])
    def post_question():
        data = request.json
        try:
            Question(question=data['question'],
                     answer=data['answer'], 
                     difficulty=data['difficulty'], 
                     category=data['category']).insert()
            print(data)
            return {
              'success': 'True'
            }
        except:
            abort(422)

    # handling search method using search method 
    # and make the query to the DB by seanding a search term word 
    # and return the typicall questions
    @app.route('/search', methods=['POST'])
    def search():
        searchTerm = request.json['searchTerm']
        questionQuery = Question.question.ilike('%'+searchTerm+'%')
        questions = Question.query.filter(questionQuery).all()
        if questions is not None:
            questions = [question.format() for question in questions]
            return {
              "questions": questions
            }, 200
        return abort(404)

    # retrieveall questions by categories by send the category ID a
    # s a variable in the route end point
    @app.route('/categories/<int:id>/questions')
    def get_by_category(id):
        try:
            category = Category.query.get(id)
            questions = Question.query.filter_by(category=category.type).all()
            questions = [question.format() for question in questions]
            return {
                "questions": questions,
                "success": "True"
            }, 200
        except:
            abort(400)


    # play a quizz game by sending a post request by the previous question 
    # and the category abd generating random question and send it back
    @app.route('/quizzes', methods=['POST'])
    def get_random_quiz_question():
        req = request.get_json()
        previous = req.get('previous_questions')
        category = req.get('quiz_category')
        if ((category is None) or (previous is None)):
            abort(400)
        if (category['id'] == 0):
            questions = Question.query.all()
        else:
            questions = Question.query.filter_by(category=category['type']).all()
        total = len(questions)

        def get_random_question():
            return questions[random.randrange(0, len(questions), 1)]

        def check_if_used(question):
            used = False
            for q in previous:
                if (q == question.id):
                    used = True

            return used

        question = get_random_question()

        while (check_if_used(question)):
            question = get_random_question()

            if (len(previous) == total):
                return jsonify({
                    'success': True
                })

        return jsonify({
            'success': True,
            'question': question.format()
        })

    # Error handler for 404 Not found error
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
          "Message": "Not found",
          "Success": "False"
        }), 404

    # Error handler for 422 unprocessable Error
    @app.errorhandler(422)
    def unproccessed(err):
        return jsonify({
            "Message": "Unpreccessable",
            "Success": "False"
        }), 422

    # Error handler for 500 server error
    @app.errorhandler(500)
    def server_error(err):
        return {
            "message": "Server Error",
            "Success": "False"
        }, 500

    # Error handler for 400 bad request
    @app.errorhandler(400)
    def bad_request(err):
        return {
            "Message": "Bad Request",
            "Success": "False"
        }, 400
    return app
