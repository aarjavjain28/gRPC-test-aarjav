import grpc
from concurrent import futures
import simple_api_pb2
import simple_api_pb2_grpc

class SimpleApiServicer(simple_api_pb2_grpc.SimpleApiServicer):
    def Greet(self, request, context):
        return simple_api_pb2.GreetResponse(greeting=f"Hello, your name is , {request.name}!")

class SquareRootApiServicer(simple_api_pb2_grpc.SquareRootApiServicer):
    def Sqrt(self, request, context):
        return simple_api_pb2.SqrtResponse(number=request.number**0.5)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    simple_api_pb2_grpc.add_SimpleApiServicer_to_server(SimpleApiServicer(), server)
    simple_api_pb2_grpc.add_SquareRootApiServicer_to_server(SquareRootApiServicer(), server)
    server.add_insecure_port('[::]:8080')
    server.start()
    print("Server started, listening on port 8080")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
