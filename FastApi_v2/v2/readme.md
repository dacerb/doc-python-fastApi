# ¿Qué es FastAPI?
> Es un framework moderno y de alto rendimiento para creación de API con Python

Características: 
- Rápido
- Menos errores
- Fácil e intuitivo
- Robusto
- Basado en estándares
- Marco utilizado por FastAPI


  - Starlette:
    - Framework asíncrono para la construcción de servicios y es uno de los más rápidos de Python
  - Pydantic: Encargado de la validación de datos. 
  - Uvicorn

# Iniciando la app en modo auto reload
``uvicorn main:app --reload ``

``uvicorn main:app --reload --port 5000``

``uvicorn main:app --reload --port 5000 --host 0.0.0.0``  ## Socket Binding Disponibilizamos la app para todas las redes.

[FastApi](https://fastapi.tiangolo.com/tutorial/first-steps/)

[Uvicorn](https://www.uvicorn.org/settings/)

