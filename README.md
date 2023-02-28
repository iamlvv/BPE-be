# BPE-BE

Set up:
```
 pip install -r requirements.txt
```
```
python manage.py runserver
```


Testing:
* GET: http://127.0.0.1:8000/evaluate/test.json
* POST: http://127.0.0.1:8000/evaluate/test.json 
```
Body:
{
    "abc": "Hello"
}
```