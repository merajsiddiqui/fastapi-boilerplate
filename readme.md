# PhysioX API

PhysioX API development in python with the help of fastAPI

## Setup

```bash
python --version

>> Python 3.8.9

```

1. ` virtualenv venv`
2. `source venv/bin/activate`
3. `pip install -r requirements.txt`
4. `cp example.app.in`

> ### Running the application
> `uvicorn main:app --reload`

# Migration

When you add a new model or alter the existing model you need to create new migration. You can create migration

```bash
 alembic revision --autogenerate -m "Users and Doctors Table added"
```

To run the migration you have created you can run the below command

```bash
 alembic revision upgrade   
```

> Note: When you are using any custom type from `sqlalchemy_utils` you need to manually add the `import sqlalchemy_utils` in revision files

# Documents

> API documents will be accessible on `/docs`