pymarket
========

A small pyramid application to study framework features and simulate a shopping cart.

Resources:

- [Pyramid](http://docs.pylonsproject.org/en/latest/);
- [mongoDB](http://www.mongodb.org/);
- [PyMongo](http://api.mongodb.org/python/current/);
- [Bootstrap](http://getbootstrap.com/).


Usage
-----

Add the mongoDB credentials in development.ini before run.

```bash
## Web application

# Inside a virtual environment
python setup.py develop
pserve development.ini
http://localhost:6543/
```