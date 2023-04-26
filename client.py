import grpc
import simple_api_pb2
import simple_api_pb2_grpc

def run():
    channel = grpc.insecure_channel('https://aarjav-grpc-test-5crxeuc6wq-nw.a.run.app:8080')
    stub = simple_api_pb2_grpc.SimpleApiStub(channel)
    response = stub.Greet(simple_api_pb2.GreetRequest(name='World'))
    print(response.greeting)

if __name__ == '__main__':
    run()
