## Swagger codegen for Python

### Installation

```bash
pip install swagger-codegen
```

### Swagger version

Currently only OpenApi 3.x (aka Swagger 3) is supported. 

### Usage example

```
# Generate Petstore Api client using 'petstore' package name.
swagger_codegen generate https://petstore3.swagger.io/api/v3/openapi.json petstore

python

Python 3.8.1 (default, Jan 23 2020, 13:58:52) 
[Clang 11.0.0 (clang-1100.0.33.16)] on darwin
Type "help", "copyright", "credits" or "license" for more information.

>>> from petstore import new_client, Configuration
>>> from swagger_codegen.api.adapter.requests import RequestsAdapter
>>> from petstore.apis.user.createUser import User
>>> client = new_client(RequestsAdapter(), Configuration(host="http://petstore3.swagger.io"))
>>> pets = client.pet.findPetsByStatus()
>>> print(pets)
[Pet(category=Category(id=1, name='Dogs'), id=69, name='aHldog', photoUrls=['string'], status='available',...]
```

You can see [example source code](https://github.com/asyncee/swagger_codegen/tree/master/example)
for [PetStore](http://petstore3.swagger.io:8080/) Api in example directory of a project.

You can test example client with following command:

```bash
# Run from project directory.
python -m example.petstore_example 
```

### Code generators (also known as renderers)

There are two code generator strategies in project:

1. Render client as usual python package via `PackageRenderer`
2. Render client as installable python package via `InstallablePackageRenderer`

You can choose what renderer to use by specifying `renderer` key in `.swagger-codegen.toml`
file. Please see `.swagger-codegen.toml.example` for allowed values.

### Known issues

- Content of generated files differs run-to-run because each time functions or data
data transfer objects ordered differently. Functionally clients stay the same, but
each time the code is generated there are large diff generated by git.
- Not fully Openapi compliant: the project was built to fulfill my personal needs: a support for FastAPI-generated schemas and I needed this feature quickly, that is why there are too many large dependencies (`schemathesis`) and incompatibilities. Anyway, I'm looking forward to fix this issues by time.
- There are may be delays in reaction to issues due to small amount of free time (however PR's with tests are merged asap).

### Work in progress

Though library gives nice results for generated API, it is still in development.
Some tests are missing. API is a subject to change until stable release.

Anyway backward compatibility will be kept as most as possible.

The code is not optimized yet and mostly dirty because the project was born
as a holiday prototype.

Also `example` directory may be out of sync with actual generated code.

### Contributors

You can see all people who helped this project [at the contributors page](https://github.com/asyncee/swagger_codegen/graphs/contributors)
