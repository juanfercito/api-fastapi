from fastapi import FastAPI, Response, HTTPException
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_202_ACCEPTED, HTTP_205_RESET_CONTENT
from models.user_connection import UserConnection
from schema.usuario_schema import UsuarioSchema

app = FastAPI()
app.title = "Users with FastAPI"
app.version = "0.0.1"
conn = UserConnection()


@app.get("/", status_code=HTTP_200_OK)
def root():
    items = []
    for data in conn.read_all():
        dictionary = {}
        dictionary["id"] = data[0]
        dictionary["nombre"] = data[1]
        dictionary["apellidos"] = data[2]
        dictionary["edad"] = data[3]
        dictionary["email"] = data[4]
        dictionary["telefono"] = data[5]
        dictionary["dni"] = data[6]
        dictionary["direccion"] = data[7]
        dictionary["ciudad"] = data[8]
        dictionary["provincia"] = data[9]

        items.append(dictionary)
    return items


@app.get("/api/usuario/{id}", status_code=HTTP_200_OK)
def get_one(id_user: str):
    dictionary = {}
    data = conn.read_one(id_user)
    dictionary["id"] = data[0]
    dictionary["nombre"] = data[1]
    dictionary["apellidos"] = data[2]
    dictionary["edad"] = data[3]
    dictionary["email"] = data[4]
    dictionary["telefono"] = data[5]
    dictionary["dni"] = data[6]
    dictionary["direccion"] = data[7]
    dictionary["ciudad"] = data[8]
    dictionary["provincia"] = data[9]

    return dictionary


@app.get("/api/usuario/by-dni/{dni}", tags=["usuarios"])
async def get_one_by_dni(dni: str):
    user_data = conn.read_one_by_dni(dni)
    if user_data:
        dictionary = {}
        dictionary["id"] = user_data[0]
        dictionary["nombre"] = user_data[1]
        dictionary["apellidos"] = user_data[2]
        dictionary["edad"] = user_data[3]
        dictionary["email"] = user_data[4]
        dictionary["telefono"] = user_data[5]
        dictionary["dni"] = user_data[6]
        dictionary["direccion"] = user_data[7]
        dictionary["ciudad"] = user_data[8]
        dictionary["provincia"] = user_data[9]
        return dictionary
    raise HTTPException(status_code=404, detail="User not found")


@app.get("/api/usuario/by_city/{city}", tags=["usuarios"], status_code=HTTP_200_OK)
async def get_one_by_city(city: str):
    user_data = conn.read_by_city(city)
    if user_data:
        return user_data
    raise HTTPException(status_code=404, detail="Match not found")


@app.get("/api/usuario/by_province/{province}", tags=["usuarios"], status_code=HTTP_202_ACCEPTED)
async def get_one_by_province(province: str):
    user_data = conn.read_by_province(province)
    if user_data:
        return user_data
    raise HTTPException(status_code=404, detail="Match not found")


@app.post("/api/insert", tags=["usuarios"], status_code=HTTP_201_CREATED)
def insert(usuario_data: UsuarioSchema):
    data = usuario_data.model_dump()
    data.pop("id")
    conn.write(data)
    return Response(status_code=HTTP_201_CREATED)


@app.put("/api/update/{dni}", tags=["usuarios"], status_code=HTTP_205_RESET_CONTENT)
def update(usuario_data: UsuarioSchema, dni: str):
    data = usuario_data.model_dump()
    data["dni"] = dni
    conn.update(data)
    return Response(status_code=HTTP_205_RESET_CONTENT)


@app.delete("/api/delete/{dni}", tags=["usuarios"])
def delete(dni: str):
    conn.delete(dni)
    return Response(status_code=HTTP_204_NO_CONTENT)
