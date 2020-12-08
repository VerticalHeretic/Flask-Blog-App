# Flask Blog Project 

Simple project made for trying out and learning basics of Flask. Made by going through the tutorial on official [side](https://flask.palletsprojects.com/en/1.1.x/tutorial) of Flask project and then extending it by myself.

## Development dependencies

To install all needed dependencies just run: 

``` 
pip install -r requirements.txt
```

## To run project 
 
Firstly you must export FLASK_APP with command: 

```
export FLASK_APP=flaskr
```

And change the dev db in __init__ to your's db -> best would be to use postgressql but others should work too while we are using sql alchemy.
After that run: 

```
flask db upgrade
```

This will create db tables etc. from migration files.
After that you should be able to start the app with: 

``` 
flask run 
```