## Swagger codegen for Python

### Installation

```bash
pip install swagger-codegen
```

### Usage example

```
# Generate Petstore Api client using 'petstore' package name.
swagger_codegen generate http://petstore.swagger.io:8080/api/v3/openapi.json petstore

python

Python 3.8.1 (default, Jan 23 2020, 13:58:52) 
[Clang 11.0.0 (clang-1100.0.33.16)] on darwin
Type "help", "copyright", "credits" or "license" for more information.

>>> from petstore import new_client, Configuration
>>> from swagger_codegen.api.adapter.requests import RequestsAdapter
>>> from petstore.apis.user.createUser import User
>>> client = new_client(RequestsAdapter(), Configuration(host="http://petstore.swagger.io:8080"))
>>> print(client.user.createUser(User(id=1, username="Swagger-Codegen")))
id=1 username='Swagger-Codegen' firstName=None lastName=None email=None password=None phone=None userStatus=0
```

You can see [example source code](https://github.com/asyncee/swagger_codegen/tree/master/example)
for [PetStore](http://petstore.swagger.io:8080/) Api in example directory of a project.

### Work in progress
Though library gives nice results for generated API, it is still in development.
Some tests are missing. API is a subject to change until stable release.

Anyway backward compatibility will be kept as most as possible.
