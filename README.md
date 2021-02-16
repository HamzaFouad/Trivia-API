# Trivia API
Trivia is a web application that helps you manage creating funny quizzes by add different questions, with different difficulty levels, to different categories. You can manage it by manipulating questions by adding/modifying/deleting any questions from the database.

## Getting Started
### Frontend
#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository.
After cloning, open your terminal and run(Inside `Frontend` folder):

```bash
npm install
```

>_tip_: **npm i** is shorthand for **npm install**

### Backend
#### Installing Dependencies
Create a virtualenv and activate it
```bash
python3 -m virtualenv trivia_env
source trivia_env/bin/activate
```
then 
```bash
pip install -r requirements.txt
```
#### Setup database
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
createdb trivia
psql trivia < trivia.psql
```

#### Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

### Tests
```bash
sh run_test.sh
```

## API Reference
* GET `/categories` fetches a dictionary of all available categories
```bash
curl -X GET http://127.0.0.1:5000/categories
```
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
* GET `/questions?page=<page_number>` fetches a paginated dictionary of questions
```bash
curl -X GET http://127.0.0.1:5000/questions?page=1
```
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
  "currentCategory": null,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
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
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```

* DELETE `/questions/<question_id>` Deletes an existing questions from the database
```bash
curl -X DELETE http://127.0.0.1:5000/questions/14
```
```json
{
  "deleted": 14,
  "success": true
}
```

* POST `/questions` Adds a new question to the database
```bash
$ curl -X POST -H "Content-Type: application/json" -d '{"question" :"QuestionSample?", "answer":"AnswerSample!", "difficulty":"1", "category":"1"}' http://127.0.0.1:5000/questions
```
```json
{
  "created": 24,
  "success": true,
  "total_questions": 19
}
```

* POST `/questions/search` Fetches all questions where containing a substring of the search-term (non-case-sensitive)
```bash
curl -X POST -H "Content-Type: application/json" -d '{"searchTerm" :"title"}' http://127.0.0.1:5000/questions
```

```json
{
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
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
  "total_questions": 2
}
```

* GET `/categories/<int:category_id>/questions` fetches all questions for the specified category
```bash
curl -X GET http://127.0.0.1:5000/categories/1/questions
```
```json
{
  "current_category": 1,
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "AnswerSample!",
      "category": 1,
      "difficulty": 1,
      "id": 24,
      "question": "QuestionSample?"
    }
  ],
  "success": true,
  "total_questions": 4
}
```