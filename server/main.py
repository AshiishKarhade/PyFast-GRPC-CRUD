from fastapi import FastAPI
from concurrent import futures
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


class Users(users_pb2_grpc.UserService):
    def GetUsers(self, request, context):
        return users_pb2.GetUsersResponse(user=[
            users_pb2.User(
                id="1",
                name="Ashish K",
                email="ashish@gmail.com",
                password="password"
            )
        ])


def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    users_pb2_grpc.add_UserServiceServicer_to_server(Users(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
