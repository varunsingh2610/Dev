# movie_api
RESTful API for movies (something similar to IMDB)

  What is it?
  -----------
  A RESTful API for movies (something similar to IMDB).
  Movies data store api that exposes the following functionality:
  
    1] There is 2 levels of access:
       Admin - who can add, remove or edit movies.
       Users - who can just view the movies.
    2] Decent search funcationality by name for movies.
    3] User can register and get access to api.
    4] Basic auth authorization for api is implemented. 


  The Version
  ------------
  This is movie_api version 0.0.1 date of this release is 14-10-2018.

  Requirement:
  ------------
    1]. Platform - Linux/ubuntu
    2]. Database - SQLite3
    3]. Python 3.6.6
    4]. Python api framework - Falcon
    6]. Gunicorn

  Deployment steps:
  -----------------
      
  1]  Run the movie_api/requirements.txt file to install dependancies 
      
      pip install -r requirements.txt 


  Run the Application
  --------------------
  Go to the movie_api directory and run run.py using gunicron
  
    gunicorn run:app --reload
  
  Use REST client or curl commnad to access the api,
  URL for api : 
    
    http://localhost:8000/api/


  Visit the running application on Heroku
  ---------------------------------------
  Use REST client or curl commnad to access the api,
  URL for api : 
    
    https://movie-imdb-api.herokuapp.com/api/

  Documentation
  -------------
    1. Refer usage.txt for usage of api
    2. Refer funct_req.txt to get to know requirement

     
 
