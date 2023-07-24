from fastapi import FastAPI

import grpc
from client.grpc_server import users_pb2_grpc, users_pb2

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/api/v1/users")
def get_users():
    response = []
    print("Will try to get the user ...")
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = users_pb2_grpc.UserServiceStub(channel)
        response = stub.GetUsers(users_pb2.GetUsersRequest())
    print(response.user)

# def run():
#     response = []
#     print("Will try to get the user ...")
#     with grpc.insecure_channel("localhost:50051") as channel:
#         stub = users_pb2_grpc.UserServiceStub(channel)
#         response = stub.GetUsers(users_pb2.GetUsersRequest())
#     print(response.user)
#
#
# if __name__ == "__main__":
#     run()