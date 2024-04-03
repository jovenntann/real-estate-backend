# real-estate-backend
This is a Real Estate Application that leverages AI for enhanced functionality.

## Setup

Follow these steps to set up the project:

1. Install Django:
   Use the following command to install Django:
   ```pip install Django```

2. Start the Django project:
   Use the following command to start the Django project:
   ```django-admin startproject tappy .```

3. Start the Django app:
   Use the following command to start the Django app:
   ```python manage.py startapp common```

# Unit Testing

Here are some instructions for running unit tests:

### Running the unit tests using coverage:
   Use the following command to run the unit tests using coverage:
   ```
   coverage run manage.py test
   docker exec -it real-estate-backend_django_1 coverage run manage.py test
   ```

### Adding verbosity (level 2 is recommended):
   Use the following command to add verbosity:
   ```
   coverage run manage.py test -v 2 --no-logs
   docker exec -it real-estate-backend_django_1 coverage run manage.py test -v 2 --no-logs
   ```

### Running a specific test case:
   Use the following command to run a specific test case:
   ```
   coverage run manage.py test domain.users.tests -v 2
   ```

### Generating the coverage report:
   Use the following commands to generate the coverage report:
   ```
   coverage html

   or

   coverage report
   ```

### Combining all test commands:
   Use the following commands to run all tests and generate a coverage report:
   ```
   docker exec -it real-estate-backend_django_1 coverage run manage.py test -v 2 --no-logs
   docker exec -it real-estate-backend_django_1 coverage html
   open htmlcov/index.html
   ```
