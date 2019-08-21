run
```
flask db init; flask db migrate; flask db upgrade; flask db upgrade; flask translate compile
```
to initialise database

then
```
gunicorn app:app
```
to start app