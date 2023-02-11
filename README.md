# doc-python-fastApi
Curso de FastAPi


FastApi implementa starlette, uvicorn, pydantic que son grandes frameworks y librerias en python.
Y les agrega mejoras.

Para comenzar debemos crear un entorno de desarrollo utilizando poetry o bien pip.

### pip y venv
```

py -m venv venv
.\venv\Scripts\activate
(venv) PS D:\CURSOS\doc-python-fastApi> deactivate   

pip install fastapi uvicorn
```

### poetry 

```
# https://python-poetry.org/docs/
poetry add fastapi uvicorn
```


Para empezar con fastapi debemos importar e instanciar, una vez realizado vamos a utilizra las path operations 

```
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def get_function():
    return "Hellow Word", 200
```

para ejecutar el server debemos ejecutar el siguiente comenado
`uvicorn main:app --reload`

el flag --reaload configura el server en [Hot Realoading](https://www.geeksforgeeks.org/difference-between-hot-reloading-and-live-reloading-in-react-native/)

```
$ uvicorn main:app --reload
INFO:     Will watch for changes in these directories: ['/Users/dacerbo/Desktop/RPS/doc-python-fastApi']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [80257] using StatReload
INFO:     Started server process [80259]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:63284 - "GET / HTTP/1.1" 200 OK
```

---

FastAPi implementa de base la documentacion de las API utilizando la especificacion de OAP
para poder acceder a la documentacion basta con ir al endpoint /docs `http://127.0.0.1:8000/docs`

Para consultar la especificación podemos hacerlo en el siguiente [LINK](http://127.0.0.1:8000/openapi.json)
> La especificación seria la definición de como funciona y queremos mostrar la documentación
```
// 20230131085752
// http://127.0.0.1:8000/openapi.json

{
  "openapi": "3.0.2",
  "info": {
    "title": "FastAPI",
    "version": "0.1.0"
  },
  "paths": {
    "/": {
      "get": {
        "summary": "Home",
        "operationId": "home__get",
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  
                }
              }
            }
          }
        }
      }
    }
  }
}
```

En FastApi tenemos Swagger UI y ReDoc, pero si tomamos la especificación la vamos a poder importar a otras plataformas de visualización.

**Para visualizar la documentacion con redoc podemos hacerlo a traves del link:** `http://127.0.0.1:8000/redoc`

---
### PATH OPERATION
path operation comprende a todo lo que viene 

### PATH PARAMETERs

### PATH, PARAMETERs, + Query Parameters