from concurrent import futures
import logging
import grpc
from grpc_server import users_pb2
from grpc_server import users_pb2_grpc

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

    def GetUserById(self, request, context):

        return users_pb2.GetUserByIdResponse()

    def CreateUser(self, request, context):
        pass

    def UpdateUser(self, request, context):
        pass

    def DeleteUser(self, request, context):
        pass

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
