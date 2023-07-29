from concurrent import futures
import logging
from fileinput import filename

import grpc
from grpc_server import users_pb2
from grpc_server import users_pb2_grpc
from database import crud

logging.basicConfig(filename="application.log", format='%(asctime)s %(message)s', filemode='w')
logger = logging.getLogger()

class Users(users_pb2_grpc.UserService):
    def GetUsers(self, request, context):
        users = crud.get_all_users()
        user_responses = [users_pb2.User(
            id=user.id,
            name=user.name,
            email=user.email,
            password=user.password
        ) for user in users]
        return users_pb2.GetUsersResponse(user=user_responses)

    def GetUserById(self, request, context):
        id = request.id
        user = crud.get_user_by_id(id)
        u = users_pb2.User(
            id=str(user.id),
            name=user.name,
            email=user.email,
            password=user.password
        )
        response = users_pb2.GetUserByIdResponse(user=u)
        return response

    def CreateUser(self, request, context):
        user = request.user
        # add user to DB
        crud.create_user(user.name, user.email, user.password)
        # create response
        response = users_pb2.CreateUserResponse(user=request.user)
        return response

    def UpdateUser(self, request, context):
        user = request.user
        logger.debug(user.name)
        updated_user = crud.update_user(user.id, user.name, user.email, user.password)
        logger.debug(updated_user.name)
        response = users_pb2.UpdateUserResponse(user=updated_user)
        return response

    def DeleteUser(self, request, context):
        id = request.id
        user = crud.delete_user(id)
        u = users_pb2.User(
            id=str(user.id),
            name=user.name,
            email=user.email,
            password=user.password
        )
        response = users_pb2.DeleteUserResponse(user=u)
        return response


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
