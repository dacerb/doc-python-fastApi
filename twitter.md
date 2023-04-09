Aporte / Sugerencia
Así como existen convenciones para la forma en la que escribimos el código, también existen convenciones para la forma en la que se nombran o se definen las rutas en los endpoints.

Dejo este link con algunas reglas de ejemplo: https://restfulapi.net/resource-naming/

URLs
Teniendo lo anterior en cuenta, sugeriría que utilicen las siguientes definiciones:

Tweets
GET /tweets/ -> Shows all tweets
GET /tweets/{id} -> Shows a specific tweet
POST /tweets/ -> Creates a new tweet
PUT /tweets/{id} -> Updates a specific tweet
DELETE /tweets/{id} -> Deletes a specific tweet
Authentication
POST /auth/signup -> Registers a new user
POST /auth/login -> Login a user
Users
GET /users/ -> Shows all users
GET /users/{id} -> Gets a specific user
PUT /users/{id} -> Updates a specific user
DELETE /users/{id} -> Deletes a specific user