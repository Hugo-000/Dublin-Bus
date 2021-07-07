### 
### This is the app for scrapper 
By default it created the following files. 
```buildoutcfg
└── scrapper
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── migrations
    │   └── __init__.py
    ├── models.py
    ├── readme.md
    ├── tests.py
    └── views.py

```


### How to set up Database for the first time

This project makes use of aws RDS. First set up a Database on AWS. And change the ```setting.py``` under backend folder.

Database part:
```buildoutcfg
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Dubin_Bus_Static',
        'USER': 'admin',
        'PASSWORD': 'Ucd-rp-2021',
        'HOST': 'dublin-bus-g1-ucd.cy0cy93b2vsn.eu-west-1.rds.amazonaws.com',
        'PORT': '3306',
    }
```

Name refers to Database Name. It refers to database name set up inside the instance of RDS. Not the name on the AWS console.
Make sure the connection is set up. 

```buildoutcfg bash
nc -zv dublin-bus-g1-ucd.cy0cy93b2vsn.eu-west-1.rds.amazonaws.com 3306
```

Then, run,

```buildoutcfg
python3 manage.py makemigrations
python3 manage.py migrate
```
Tables and columns should be set. 




