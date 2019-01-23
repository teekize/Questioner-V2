[![Maintainability](https://api.codeclimate.com/v1/badges/a882fd1c5c0afc243da7/maintainability)](https://codeclimate.com/github/teekize/Questioner-V2/maintainability)


[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/5ecdc75d858e2c260a23)

## Questionner

Crowd-source questions for a meetup. Questioner helps the meetup organizer prioritize questions to be answered. Other users can vote on asked questions and they bubble to the top or bottom of the log

## Getting started
This will give you what you need for the aplication to run locally

## Requirements

1. python 3.7
2. Postman
3. Git

## Installing 
 1.clone this repository
 [repo](https://github.com/teekize/Questionner.git)
 have the python installed in your machine
 
 3. Install a virtual environment
 this command is for windows
 `pip venv venv`

 4. Then you activate the virtual envirionmnet
 this is for windows
 `venv\Scripts\activate`

 5. To test the api in your local machine
 install the the reuirements file 
 `pip install -r requirements.txt`

 6. To run the application 
 run the `run.py` file 

 Then test all the endpoinst using POSTMAN
## Endpoints
 | Method  	|   Endpoint	                            |  Description 	    |
|---	    |---	                                    |---	            |
|  POST 	| `/api/v1/meetups`  	                        |   this endpoint adds a new meetup	    |   
|   GET	    | `/api/v1/meetups/<meetup_id> `          |   this endpoint gets you a specific meetup	|
|  GET 	    | `/api/v1/meetups/upcoming`	                |   this endpoint gets all upcoming meetups	|
|  POST	    | `api/v1/questions`	                        |   this endpints creates a new question	|
|  PATCH 	| `/api/v1/questions/<question_id>/upvote`|   this endpoint upvotes a question	|
|  PATCH 	| `/api/v1/questions/<question_id>/downvote`|  this endpoint  downvotes a question	|
|  POST 	| `/api/v1/meetups/<meetup_id>/rsvp` 	      |   this questions create an rsvp response	|


[Heroku link](https://questionner-v1-teeka.herokuapp.com/)
## Author 
Teeka Elvis
