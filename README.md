# FyleAssignment
A REST service that can fetch bank details, using the data given in the API’s query parameters. The API uses JWT for authentication.
It has been created in **Python** using **Flask** framework. The database has been created with **PostgreSQL**.
This API has been deployed on [Heroku](https://bank-data-proj-api-heroku.herokuapp.com/).

## Endpoints

- ### **_/registration_**</br>
  To register new users

  **Method**: **POST**</br>
  **Body**: {'username':'fyle','password':'fyle'}</br>
    
 ```
 curl -X POST \
  https://bank-data-proj-api-heroku.herokuapp.com/registration \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: 1c602bee-d015-4612-bc6a-242af20a967b' \
  -H 'cache-control: no-cache' \
  -d '{
    "username": "fyle",
    "password": "fyle"
}'
```
- ### **_/login_**</br> 
  To login for existing users

  **Method**: **POST**</br>
  **Body**: {'username':'fyle','password':'fyle'}</br>
    
 ```
 curl -X POST \
  https://bank-data-proj-api-heroku.herokuapp.com/login \
  -H 'Content-Type: application/json' \
  -H 'Postman-Token: ec79264f-852d-4e25-ad5c-29783a5a8c4e' \
  -H 'cache-control: no-cache' \
  -d '{
    "username": "fyle",
    "password": "fyle"
}'
```
- ### **_/bankifsc_**</br> 
  To fetch Bank details based on IFSC

  **Method**: **GET**</br>
  **Parameters**:ifsc</br>
 
```
curl -H "Authorization: Bearer %ACCESS%" "https://bank-data-proj-api-heroku.herokuapp.com/bankifsc?ifsc=UTBI0PBZD72"
```

- ### **_/branchesquery_**</br> 
  To fetch details of all branches for a given bank name and city

  **Method**: **GET**</br>
  **Parameters**:name, city , \<page\>, \<size\></br>
  _Page and Size are optional parameters. Size indicates LIMIT and page indicates OFFSET._

```
curl -H "Authorization: Bearer %ACCESS%" "https://bank-data-proj-api-heroku.herokuapp.com/branchesquery?name=UNITED%20BANK%20OF%20INDIA&city=BANGALORE"
```

- ### **_/branches_**</br> 
  To fetch branches table

  **Method**: **GET**</br>
  **Parameters**:\<page\>, \<size\></br>
  _Page and Size are optional parameters. Size indicates LIMIT and page indicates OFFSET._
  It fetches entire table if page and size parameters are not specified.

```
curl -X GET \
  'https://bank-data-proj-api-heroku.herokuapp.com/branches?page=5&size=20' \
  -H 'Postman-Token: 75e22f7f-3abe-4914-b9fa-697ce0f95181' \
  -H 'cache-control: no-cache'
```

- ### **_/banks_**</br> 
  To fetch banks table

  **Method**: **GET**</br>
  **Parameters**:\<page\>, \<size\></br>
  _Page and Size are optional parameters. Size indicates LIMIT and page indicates OFFSET._
  It fetches entire table if page and size parameters are not specified.

```
curl -X GET \
  'https://bank-data-proj-api-heroku.herokuapp.com/banks?page=5&size=20' \
  -H 'Postman-Token: 06fb27ec-69af-4c78-9058-8f7dd9e62e82' \
  -H 'cache-control: no-cache'
```

- ### **_/logout/access_**</br> 
    To revoke access token
- ### **_/logout/refresh_**</br> 
    To revoke refresh token
- ### **_/token/refresh_**</br> 
    To generate new access token from refresh token
- ### **_/secret_**</br> 
    Testing route for JWT

```
Routes /secret, /bankifsc, /branchesquery are protected routes.
```
  
