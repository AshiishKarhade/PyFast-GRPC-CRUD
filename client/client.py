from fastapi import FastAPI

import grpc
from grpc_server import users_pb2
from grpc_server import users_pb2_grpc

app = FastAPI()
grpc_server_host = "grpc_server"

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/api/v1/users")
def get_users():
    with grpc.insecure_channel(f"{grpc_server_host}:50051") as channel:
        stub = users_pb2_grpc.UserServiceStub(channel)
        response = stub.GetUsers(users_pb2.GetUsersRequest())
    print(response.user)


@app.get("/api/v1/user/{id}")
def get_user_by_id(id: int):
    with grpc.insecure_channel(f"{grpc_server_host}:50051") as channel:
        stub = users_pb2_grpc.UserServiceStub(channel)
        response = stub.GetUserById(users_pb2.GetUserByIdRequest(id=str(id)))
    print(response.user)


@app.post("/api/v1/createuser")
def create_user(user_data: dict):
    user = users_pb2.User(
        name=user_data.get("name"),
        email=user_data.get("email"),
        password=user_data.get("password")
    )
    with grpc.insecure_channel(f"{grpc_server_host}:50051") as channel:
        stub = users_pb2_grpc.UserServiceStub(channel)
        response = stub.CreateUser(users_pb2.CreateUserRequest(user=user))
    print(response.user)


@app.put("/api/v1/updateuser/{id}")
def update_user(id: int, user_data: dict):
    print("Updating...")
    user = users_pb2.User(
        id=str(id),
        name=user_data.get("name"),
        email=user_data.get("email"),
        password=user_data.get("password")
    )
    # print(user.id)
    with grpc.insecure_channel(f"{grpc_server_host}:50051") as channel:
        stub = users_pb2_grpc.UserServiceStub(channel)
        response = stub.UpdateUser(users_pb2.UpdateUserRequest(user=user))
    print(response.user)


@app.delete("/api/v1/deleteuser/{id}")
def delete_user(id: int):
    with grpc.insecure_channel(f"{grpc_server_host}:50051") as channel:
        stub = users_pb2_grpc.UserServiceStub(channel)
        response = stub.DeleteUser(users_pb2.DeleteUserRequest(id=str(id)))
    print(response.user)