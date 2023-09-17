Trivia API - Backend
-----

## Main Files: Project Structure

  ```sh
  ├── README.md
  ├── flaskr
  │   ├── __init.py__ 
  ├── models.py
  ├── requirements.txt
  ├── test_flaskr.py
  ├── trivia.psql
  ```

## Setting up the Backend

  First, Follow instructions to install the latest version of python for your platform in the [python Documentation](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python) or [install Python](https://www.python.org/downloads/) and [install PostgreSQL](https://www.postgresql.org/download/) if you haven't already.

  To start and run the local development server,

  1. Initialize and activate a virtual environment:

    We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

    ```
    $ cd YOUR_PROJECT_DIRECTORY_PATH/
    $ py -3 -m venv env
    $ env\Scripts\activate
    ```

  2. PIP Dependencies:
    
    Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory.

    ```
    $ cd backend/
    $ py -m pip install -r requirements.txt
    ```

  3. Set up the Database:

    With Postgres running, create a `trivia` database:

    ```
    $ createdb trivia
    ```

    Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

    ```
    $ psql trivia < trivia.psql
    ```

  5. Run the Server:

    From within the `YOUR_PROJECT_DIRECTORY_PATH/` directory first ensure you are working using your created virtual environment.

    To run the server, execute:

    ```
    $ flask run --reload
    ```

    The `--reload` flag will detect file changes and restart the server automatically.

    /

    ```
    $ flask --app flaskr run
    ```

## Setting up the Testing

  To deploy the tests, run

  ```
  $ dropdb trivia_test
  $ createdb trivia_test
  $ psql trivia_test < trivia.psql
  $ python test_flaskr.py
  ```

## API Documentation For Trivia

  `GET '/categories'`

  - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
  - Request Arguments: None
  - Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.

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

  ----------------------------------------------------------------------------

  `GET '/questions?page=${integer}'`

  - Fetches a paginated set of questions, a total number of questions, all categories and current category string.
  - Request Arguments: `page` - integer
  - Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string

  ```json
  {
    "questions": [
      {
        "id": 1,
        "question": "This is a question",
        "answer": "This is an answer",
        "difficulty": 5,
        "category": 2
      }
    ],
    "total_questions": 100,
    "categories": {
      "1": "Science",
      "2": "Art",
      "3": "Geography",
      "4": "History",
      "5": "Entertainment",
      "6": "Sports"
    },
    "current_category": "",
    "success": true
  }
  ```

  ----------------------------------------------------------------------------

  `DELETE '/questions/${id}'`

  - Deletes a specified question using the id of the question
  - Request Arguments: `id` - integer
  - Returns: Does not need to return anything besides the appropriate HTTP status code. Optionally can return the id of the question. If you are able to modify the frontend, you can have it remove the question using the id instead of refetching the questions.

  ```json
  {
    "success": true
  }
  ```

  ----------------------------------------------------------------------------

  `POST '/questions'`

  - Sends a post request in order to add a new question
  - Request Body:

  ```json
  {
    "question": "Heres a new question string",
    "answer": "Heres a new answer string",
    "difficulty": 1,
    "category": 3
  }
  ```

  - Returns: Does not return any new data

  ```json
  {
    "success": true
  }
  ```

  ----------------------------------------------------------------------------

  `POST '/questions/search'`

  - Sends a post request in order to search for a specific question by search term
  - Request Body:

  ```json
  {
    "searchTerm": "this is the term the user is looking for"
  }
  ```

  - Returns: any array of questions, a number of totalQuestions that met the search term and the current category string

  ```json
  {
    "questions": [
      {
        "id": 1,
        "question": "This is a question",
        "answer": "This is an answer",
        "difficulty": 5,
        "category": 5
      }
    ],
    "total_questions": 100,
    "current_category": "",
    "success": true
  }
  ```

  ----------------------------------------------------------------------------

  `GET '/categories/${id}/questions'`

  - Fetches questions for a cateogry specified by id request argument
  - Request Arguments: `id` - integer
  - Returns: An object with questions for the specified category, total questions, and current category string

  ```json
  {
    "questions": [
      {
        "id": 1,
        "question": "This is a question",
        "answer": "This is an answer",
        "difficulty": 5,
        "category": 4
      }
    ],
    "total_questions": 100,
    "current_category": "History",
    "success": true
  }
  ```

  ----------------------------------------------------------------------------

  `POST '/quizzes'`

  - Sends a post request in order to get the next question
  - Request Body:

  ```json
  {
    'previous_questions': [1, 4, 20, 15],
    'quiz_category': 'current category'
  }
  ```

  - Returns: a single new question object

  ```json
  {
    "question": {
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 4
    },
    "success": true
  }
  ```

  ----------------------------------------------------------------------------

  `400 - Bad Request`

  - Returns: Errors are returned as JSON objects.

  ```json
  {
    "error": 400,
    "message": "Bad Request",
    "success": false
  }
  ```

  ----------------------------------------------------------------------------

  `404 - Not Found`

  - Returns: Errors are returned as JSON objects.

  ```json
  {
    "error": 404,
    "message": "Not Found",
    "success": false
  }
  ```

  ----------------------------------------------------------------------------

  `422 - Unprocessable Entity`

  - Returns: Errors are returned as JSON objects.

  ```json
  {
    "error": 422,
    "message": "Unprocessable Entity",
    "success": false
  }
  ```

  ----------------------------------------------------------------------------

  `405 - Method Not Allowed`

  - Returns: Errors are returned as JSON objects.

  ```json
  {
    "error": 405,
    "message": "Method Not Allowed",
    "success": false
  }
  ```

  ----------------------------------------------------------------------------

  `500 - Internal Server Error`

  - Returns: Errors are returned as JSON objects.

  ```json
  {
    "error": 500,
    "message": "Internal Server Error",
    "success": false
  }
  ```
