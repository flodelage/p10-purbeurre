# Pur Beurre
This application is the eighth project of the OpenClassrooms' Python developer course.
Site en production sur Heroku: https://p8-pur-beurre.herokuapp.com/

## Application description
The application aims to allow a user to find products with a better nutrition grade than a chosen product.

### Features
* Account creation
* Login / Logout
* Search and display a product or products from a category by entering a name
* Display a product details (nutrition grade, nutrient intake, link to the Openfoodfacts page)
* Display substitutes list (products with a better nutrition grade than a chosen product)
* Save a substitute as favorite
* Display favorites
* Delete substitute from favorites

### Technologies
* Python / Django
* PostgreSQL
* Media Wiki API

## Getting started
1. Clone the repository:
```
git clone https://github.com/flodelage/pur-beurre.git
```

2. Create virtual environnement:
```
python3 -m venv env
```

3. Activate virtual environnement:
```
source env/bin/activate
```

4. Install requirements:
```
pip install -r requirements.txt
```

5. Update pur_beurre/settings.py:
DATABASES = {
    'default': {
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
    }
}

6. populate the database:
```
python manage.py populate_db
```

7. Run the project in local:
```
python manage.py runserver
```

8. Go to your browser in order to access the localhost at the URL (by default):
```
http://127.0.0.1:8000/
```

## Running tests
```
python manage.py test
```
