# Full Stack Trivia API Backend

## Getting Started
This app is a game for getting questions from API ,and this API is used in frontend side to be like a game to try answering this questions 

### Installing Dependencies
For the front end installing dependecies for react app 

```npm start```

For installing librearies used in flask app

```pip install -r requirements```

#### local devlopment
For running the frondend app

```npm start```

For running the server 

```
export APP_FLASK=flaskr
export APP_ENV=development
flask run
```

## API Testing
run these commands
```
dropdb trivia
createdb trivia
psql trivia < trivia.psql
python test_flaskr.py
```


### API Refernces
* Base URL ```https:\\localhost:5000```

### Error handling
The error will return as JSON object like:
```
{
    "message": "Server Error",
    "Success":"Fasle"
}
```
Types off error:
* 400 - bad request
* 404 - not found
* 422 - unproccessable
* 500 - server error


### End points
#### GET /categories
* General :
  * return a list of categories .
* curl ```https:\\localhost:5000\categories```

```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }
}
```

#### GET /questions
* General :
  * Return a list contains questions.
* curl ```https:\\localhost:5000\questions```


```
{
  "categories": "categories", 
  "currentCategory": "All", 
  "questions": [
    {
      "answer": "yes", 
      "category": "Science", 
      "difficulty": 1, 
      "id": 9, 
      "question": "Whose autobiography is entitled 'I Know Why the Cagad Bird Sings'?"
    }
  ]
    total_questions:10
}
```

#### POST /questions
* General :
  * Create a new question to add to the questions list .
  * return a JSON object with message success .
* Sample: curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{ "question": "Which US state contains an area known as the Upper Penninsula?", "answer": "Michigan", "difficulty": 5, "category": "Geography" }'
```
{
    'success':'true'
}
```

#### DELETE /questions/<int:id>
* General : 
  * Delete the current question id from the questions list
  * Rerurn with message as JSON success
* ```curl http://127.0.0.1:5000/questions/6 -X DELETE```

```
{
    "sucess":"true"
}
```

#### POST /search
* General : 
  * post the keyword to search about it in the question list .
  * return a JOSN Object with all questions that contsains the search word .
* ```curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "club"}'```

#### GET /categories/<int:id>/questions
* General :
  * Get the questions by its category .
  * return the list of the specific category as json .
* ```curl http://127.0.0.1:5000/categories/1/questions```

```
{
  "questions": [
    {
      "answer": "yes", 
      "category": "Science", 
      "difficulty": 1, 
      "id": 9, 
      "question": "Whose autobiography is entitled 'I Know Why the Cagad Bird Sings'?"
    }
  ]
}
```

#### POST /qizzez
* Generally :
  * allow users to play a quiz gane.
  * return with random questions of maximum 5 questions .
* ```url http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [1, 2], "quiz_category": {"type": "Science", "id": "1"}}'```
```
{
      "question": {
          "answer": "Blood", 
          "category": 1, 
          "difficulty": 4, 
          "id": 22, 
          "question": "Hematology is a branch of medicine involving the study of what?"
      }, 
      "success": true
  }```