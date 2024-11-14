# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the project repository and [clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

### Backend

The [backend](./backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with `TODO`. These are the files you'd want to edit in the frontend:

1. `frontend/src/components/QuestionView.js`
2. `frontend/src/components/FormView.js`
3. `frontend/src/components/QuizView.js`

By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API.

> View the [Frontend README](./frontend/README.md) for more details.

## Error Handling

Errors are returned as JSON objects in the following format:
    {
        "success": False, 
        "error": 404,
        "message": "Resource not found"
    }

The API will return four error types when requests fail:

* 400: Bad Request
* 404: Resource Not Found
* 422: Request contains invalid data
* 500: Server error

## Endpoints

`GET '/categories'`

* Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category

* Request Arguments: None

* Returns: An object with a key, `categories`, that contains an object of `id: category_string` key: value pairs, and a key, `success`, with value `true`

Sample: `curl http://127.0.0.1:5000/categories`

```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    }, 
    "success": true
}
```

`GET '/questions'`

* Fetches a paginated list of questions, total number of questions available, dictionary of all categories and string of the current category

* Request Arguments: provide page as an integer starting from one 

* Returns: An object with a key, `questions`, that contains a list of up to 10 question objects,  a key, `categories`, that contains an object of `id: category_string` key: value pairs, a key `currentCategory` that contains the current `category_string`, a key `totalQuestions` that contains the integer value of number of total questions, and a key `success` with value `true`

Sample: `curl http://127.0.0.1:5000/questions?page=1`

```json
{
    "questions": [
        {
          "answer": "Apollo 13",
          "category": 5,
          "difficulty": 4,
          "id": 2,
          "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
          "answer": "Tom Cruise",
          "category": 5,
          "difficulty": 4,
          "id": 4,
          "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
    ],
    "currentCategory": null,
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true,
    "totalQuestions": 21
}
```

`DELETE '/questions/{question_id}'`

* Deletes the question of given ID, if it exists.

* Request Arguments: None

* Returns: An object with a key, `questions`, that contains a list of up to 10 question objects, and a key `success` with value `true`

Sample: `curl -X DELETE http://127.0.0.1:5000/questions/2`

```json
{
    "questions": [
        {
          "answer": "Tom Cruise",
          "category": 5,
          "difficulty": 4,
          "id": 4,
          "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"                
        },
        {
          "answer": "Edward Scissorhands",
          "category": 5,
          "difficulty": 3,
          "id": 6,
          "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
          "answer": "Brazil",
          "category": 6,
          "difficulty": 3,
          "id": 10,
          "question": "Which is the only team to play in every soccer World Cup tournament?"
        }
    ],
    "success": true
}
```

`POST '/questions'`

* Creates a new question using the submitted question, answer, category, and difficulty. Request body:

```json
{
    "question":"What is the answer?", 
    "answer":"This is the answer", 
    "category":"1", 
    "difficulty":"3"
}
```

* Request Arguments: None

* Returns: A single key `success` with value `true`

Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"What is the answer?", "answer":"This is the answer", "category":"1", "difficulty":"3"}'`

```json
{
    "success": true
}
```

`POST '/questions'`

* Sends a post request to search for questions that include the given search term submitted. Request body:

```json
{
    "searchTerm":"Find this"
}
```

* Request Arguments: None

* Returns: An object with a key, `questions`, that contains a list of question objects where the `question` value includes the given search term, a key `currentCategory` that contains the current `category_string`, a key `totalQuestions` that contains the integer value of number of total questions that match the search term, and a key `success` with value `true`

Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"soccer"}'`

```json
{
    "questions": [
        {
          "answer": "Brazil",
          "category": 6,
          "difficulty": 3,
          "id": 10,
          "question": "Which is the only team to play in every soccer World Cup tournament?"    
        },
        {    
          "answer": "Uruguay",
          "category": 6,
          "difficulty": 4,
          "id": 11,
          "question": "Which country won the first ever soccer World Cup in 1930?"
        }
    ],
    "success": true,
    "totalQuestions": 2,
    "currentCategory": null,
}
```

`GET '/categories/{category_id}/questions'`

* Fetches a list of questions that match the category of the given category ID

* Request Arguments: None

* Returns: An object with a key, `questions`, that contains a list of question objects where the `category` value matches the given `category_id`, a key `currentCategory` that contains the current `category_string` based on the given `category_id`, a key `totalQuestions` that contains the integer value of number of total questions that match the search term, and a key `success` with value `true`

Sample: `curl http://127.0.0.1:5000/categories/5/questions`

```json
{
    "questions": [
        {
          "answer": "Tom Cruise",
          "category": 5,
          "difficulty": 4,
          "id": 4,
          "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"                
        },
        {
          "answer": "Edward Scissorhands",
          "category": 5,
          "difficulty": 3,
          "id": 6,
          "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        }
    ],
    "success": true,
    "totalQuestions": 2,
    "currentCategory": "Art",
}
```

`POST '/quizzes'`

* Sends a post request to search for questions within the given category and not from the list of previous question IDs. Request body:

```json
{
    "previous_questions": [1,5,7],
    "quiz_category": {
        "id": "1",
        "type": "Science"
    }
}
```

* Request Arguments: None

* Returns: A `question` key with a single randomly selected new question object as value, and a key `success` with value `true`

Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"previous_questions":[1,5,7], "quiz_category":{"id": "1", "type": "Science"}}'`

```json
{
    "question": {
        "answer": "The Liver",
        "category": 1,
        "difficulty": 4,
        "id": 20,
        "question": "What is the heaviest organ in the human body?"
    },
    "success": true
}
```


