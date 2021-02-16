from flask import Flask, json, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from werkzeug import exceptions
from models import setup_db, Question, Category

OK = 200
CREATED = 201
BAD_REQUEST = 400
NOT_FOUND = 404
NOT_PROCESSABLE = 422

QUESTIONS_PER_PAGE = 10

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


def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start =  (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions


def select_random_elem(elements):
  return elements[random.randint(0, len(elements)-1)]


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  CORS(app, resources={r"/api/*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    # response.headers.add('Access-Control-Allow-Headers', 'GET, PUT, POST, DELETE, OPTIONS')
    return response


  @app.route('/categories', methods=['GET'])
  def get_all_categories():
    categories = Category.query.order_by(Category.id).all()
    
    if len(categories) == 0:
      abort(NOT_FOUND)
    
    categories_formatted = {category.id: category.type for category in categories}

    return jsonify({
      'success': True,
      'categories': categories_formatted
    }), OK
  

  @app.route('/questions', methods=['GET'])
  def get_page_of_questions():

    questions = Question.query.all()
    categories = Category.query.all()

    page_of_questions = paginate_questions(request, questions)
    categories_formatted = {category.id: category.type for category in categories}

    # if len(page_of_questions) == 0:     # it is okay to be empty at some point.
    #   abort(NOT_FOUND)

    return jsonify({
    'success': True,
    'questions': page_of_questions,
    'total_questions': len(questions),
    'categories': categories_formatted,
    'currentCategory': None
    }), OK


  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):

    question = Question.query.get(question_id)

    if not question: # Empty --- question_id not found
      abort(NOT_FOUND)

    try:
      question.delete()
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'deleted': question_id,
      }), OK
    except:
      abort(NOT_PROCESSABLE)


  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()
  
    question = body.get('question', None)
    answer = body.get('answer', None)
    difficulty = body.get('difficulty', None)
    category = body.get('category', None)
    search_term = body.get('searchTerm', None)


    if search_term: # if user applied Search - process goes here
      print(f'{Color.RED}\nSearchTerm: {search_term}{Color.END}')
      queried_questions = Question.query.filter(
          Question.question.ilike(f'%{search_term}%')
          ).all()
      
      # if len(queried_questions) == 0:
      #   abort(NOT_FOUND)
          
      page_of_questions = paginate_questions(request, queried_questions)
    
      return jsonify({
        'success': True,
        'questions': page_of_questions,
        'total_questions': len(Question.query.all())
      }), OK

    else: # if user Created a question process goes here
      # print(f'{Color.RED}\nquestion:{question}\nanswer:{answer}\ndifficulty:{difficulty}\ncategory:{category}{Color.END}')
      if None in (question, answer, difficulty, category):
        abort(BAD_REQUEST)

      created_question = Question( 
                          question=question,
                          answer=answer,
                          difficulty=difficulty,
                          category=category
                        )
      created_question.insert()
      
      return jsonify({
        'success': True,
        'created': created_question.id,
        'total_questions': len(Question.query.all())
      }), CREATED

  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_categories(category_id):

    category = Category.query.get(category_id)

    if category is None:
      abort(BAD_REQUEST)

    questions = Question.query.filter_by(category=category_id).all()
    questions_formatted = paginate_questions(request, questions)

    # if len(questions_formatted) == 0:
      #   abort(NOT_FOUND)

    return  jsonify({
      'success': True,
      'questions': questions_formatted,
      'total_questions': len(questions),
      'current_category': category_id
    }), OK


  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    found = True
    body = request.get_json()

    previous_questions = body.get('previous_questions', None)
    category = body.get('quiz_category', None)
    questions = None

    if None in (previous_questions, category):
      abort(BAD_REQUEST)
    
    
    if category['id'] == 0: # if selected 'ALL' >>> load all questions
      questions = Question.query.all()
    else: # else get the questions corresponding to the selected category
      questions = Question.query.filter_by(category=category['id']).all()

    next_question = select_random_elem(questions)

    while found:
      if next_question.id in previous_questions:
        next_question = select_random_elem(questions)
      else:
        found = False

    return jsonify({
      'success': True,
      'question': next_question.format()
    }), OK


  @app.errorhandler(BAD_REQUEST)
  def bad_request(error):
      return jsonify({
          "success": False,
          "error": BAD_REQUEST,
          "message": "BAD REQUEST"
      }), BAD_REQUEST

  @app.errorhandler(NOT_FOUND)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": NOT_FOUND,
      "message": "RESOURCE NOT FOUND"
      }), NOT_FOUND

  @app.errorhandler(NOT_PROCESSABLE)
  def unprocessable(error):
      return jsonify({
          "success": False,
          "error": NOT_PROCESSABLE,
          "message": "NOT PROCESSABLE"
      }), NOT_PROCESSABLE


  return app

    