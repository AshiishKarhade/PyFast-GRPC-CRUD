from fastapi import FastAPI

import logging
import grpc
import users_pb2
import users_pb2_grpc

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


def run():
    response = []
    print("Will try to get the user ...")
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = users_pb2_grpc.UserServiceStub(channel)
        response = stub.GetUsers(users_pb2.GetUsersRequest())
    print(response.user)


if __name__ == "__main__":
    run()