from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

# method to paginate questions
def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    formatted_questions = [question.format() for question in selection]
    return formatted_questions[start:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/*": {"origins": "*"}})
    with app.app_context():
        db.create_all()

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()

        if len(categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': {category.id: category.type for category in categories}
        })


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    """
    @app.route('/questions', methods=['GET'])
    def get_questions():
        questions = Question.query.all()

        # get the paginated questions from created method
        current_questions = paginate_questions(request, questions)
        
        # raise 404 error if no questions in given pagination
        if len(current_questions) == 0:
            abort(404)

        categories = Category.query.all()

        # set to the category type string of the first question in questions list
        current_category = Category.query.filter(Category.id == current_questions[0]["category"]).first().type
        
        return jsonify({
            'success': True,
            'questions': current_questions,
            'totalQuestions': len(questions),
            'categories': {category.id: category.type for category in categories},
            'currentCategory': current_category

        })
    
    """
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            question.delete()
            questions = Question.query.all()

            # get the paginated questions from created method
            current_questions = paginate_questions(request, questions)

            return jsonify(
                {
                    "success": True,
                    "questions": current_questions
                }
            )
        # raise 422 error if unable to complete delete request
        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=["POST"])
    def create_question():
        try:
            # Get the JSON request to create new question
            body = request.get_json()

            new_question = body.get("question", None)
            new_answer = body.get("answer", None)
            new_category = body.get("category", None)
            new_difficulty = body.get("difficulty", None)
            search = body.get("searchTerm")

            # return response for search if searchTerm available in body
            if search:
                questions = Question.query.filter(Question.question.ilike(f'%{search.lower()}%')).all()

                current_questions = paginate_questions(request, questions)

                current_category = None if current_questions == [] else Category.query.filter(Category.id == current_questions[0]["category"]).first().type

                return jsonify(
                    {
                        "success": True,
                        'questions': current_questions,
                        'totalQuestions': len(current_questions),
                        'currentCategory': current_category
                    }
                )
            # return response for creating new question if searchTerm not in body
            else:
                question = Question(question=new_question, answer=new_answer, 
                                    category=new_category, difficulty=new_difficulty)
                question.insert()

                return jsonify(
                    {
                        "success": True
                    }
                )

        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """ 
        

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def get_questions_in_category(category_id):
        category = Category.query.filter(Category.id == category_id).one_or_none()
        questions = Question.query.filter(Question.category == category_id).all()
        # raise 404 error is question with given category does not exist
        if len(questions) == 0:
            abort(404)

        # get the paginated questions from created method
        current_questions = paginate_questions(request, questions)

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "totalQuestions": len(current_questions),
                "currentCategory": category.type
            }
        )

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route("/quizzes", methods=["POST"])
    def get_quiz_questions():
        try:
            # Get the JSON request to create new question
            body = request.get_json()

            prev_questions = body.get("previous_questions")
            quiz_category = body.get("quiz_category")['id']

            # get questions left 
            questions = Question.query.filter(Question.id.not_in(prev_questions))

            # filter by category if category is given
            if quiz_category != 0:
                questions = questions.filter(Question.category == quiz_category)
            
            questions = questions.all()

            # pick random question if any available
            random_question = None if len(questions) == 0 else random.choice(questions).format()

            return jsonify(
                {
                    "success": True,
                    'question': random_question
                }
            )
        except:
            abort(400)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return ( 
            jsonify({
                "success": False,
                "error": 404,
                "message": "Resource not found"
        }), 
        404) 
    
    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({
                "success": False, 
                "error": 422, 
                "message": "Request contains invalid data"
            }),
            422)
    
    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({
                "success": False, 
                "error": 400, 
                "message": "Bad request"
            }),
            400)
    
    @app.errorhandler(500)
    def server_error(error):
        return (
            jsonify({
                "success": False, 
                "error": 500, 
                "message": "Server error"
            }),
            500)

    return app

