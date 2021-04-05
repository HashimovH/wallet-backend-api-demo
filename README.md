# wallet-backend
Paxful Python Developer Test Assignment.

### Features

- Register user to get an Authentication token for further requests.
- Create User wallet. (Starting amount 1 BTC)
- Send Money to other wallet.
- Get the statistics about profit (For admin user)

### Development Process
To begin with, I opted for Django in order to create back-end API for this assignment. More specifically, Django has 'djangorestframework' package to deal with REST API architecture. 
My django project has one `api` app which contains the functionality for API. The app uses DefaultRouter class from `rest_framework.routers`. User model has been updated because I wanted to make email field as main identifier instead of username.
Authentication token is `TokenAuthentication`  class that is simple token-based HTTP Authentication scheme.
### Executing in local computer
First of all, clone the repository:
`git clone https://github.com/HashimovH/wallet-backend.git`

Then go to cloned folder:
`cd wallet-backend`

Use docker to run the application:
`docker-compose up -d --build`

Migrate DB changes:
`docker-compose exec web python3 manage.py migrate --noinput`

**Done :)**
### API Calls
In order to see the documentation, you can use following URL.
`http://127.0.0.1:8000/api/`

However, except registration, all requests needs an Token. 

If you want to send request, Add `Authorization` as an header, and
`Token <your-token>` as a value.

POST Parameters should be in **Multipart Form** Structure.

### References
- https://www.django-rest-framework.org/
- https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/

### Thank you for reading and Enjoy the API :)
