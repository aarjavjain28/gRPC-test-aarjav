
import grpc
import simple_api_pb2
import simple_api_pb2_grpc
import logging
import json
import os
logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO
)

metadata = [("authorization","Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6Ijg2OTY5YWVjMzdhNzc4MGYxODgwNzg3NzU5M2JiYmY4Y2Y1ZGU1Y2UiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIzMjU1NTk0MDU1OS5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsImF1ZCI6IjMyNTU1OTQwNTU5LmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTAxODg1MzAwNTk3OTMyNjA3MDg2IiwiaGQiOiJ0aGVodXRncm91cC5jb20iLCJlbWFpbCI6ImFhcmphdi5qYWluMjhAdGhlaHV0Z3JvdXAuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF0X2hhc2giOiJRbDhabXRBeUUwZ285R3VaXzhaS0RnIiwiaWF0IjoxNjgyNDEyMTg4LCJleHAiOjE2ODI0MTU3ODh9.Y4KGSzNWsgQ5O2OGZv-GMF7NolyaYU9mbT0Woqokz3RxBSI3rOJ4gfljLO4YG7s-5VklL_EjR2KdHI8kMVmENY0-zNWHHV78-d3-uexsKFtyy1_Edmfpp4FzdTQr8dsyXkXsXXOydO2wCjH0nWMwiAL0qpkKz0w6VCXhV9jZkgtGjl7yR6MLLcT3V6U35tdSbQeDAVRDInqRYLzwowQlGJ_o22tibyPmwZ310cjZNozP3VPA3gchFbnblFM4T4ce2TV3wOkE-FPEtkwlEhkiSrCGEItvOv2IWX0hSNB2MSlkzHb5gxivnmLP_ueYKiWOUljE4j3ETPyqdVFTrVP7Rg" )]
HOST = "aarjav-grpc-test-5crxeuc6wq-nw.a.run.app"
with grpc.secure_channel(HOST, grpc.ssl_channel_credentials()) as channel:
    stub1 = simple_api_pb2_grpc.SimpleApiStub(channel)
    stub2 = simple_api_pb2_grpc.SquareRootApiStub(channel)
    response1 = stub1.Greet(simple_api_pb2.GreetRequest(name='World'), metadata=metadata)
    logging.info(response1)
    response2 = stub2.Sqrt(simple_api_pb2.SqrtNumber(number=16.0), metadata=metadata)
    logging.info(response2)


# class SimpleApiServicer(simple_api_pb2_grpc.SimpleApiServicer):
#
#     def Greet(self, request, context):
#         name = request.name
#         return simple_api_pb2.GreetResponse(greeting=f'Hello, {name}!')
#
# class SquareRootApiServicer(simple_api_pb2_grpc.SquareRootApiServicer):
#
#     def Sqrt(self, request, context):
#         number = request.numb
#         result = number ** 0.5
#         return simple_api_pb2.SqrtResult(number=result)
#
# def serve():
#     server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
#     api_pb2_grpc.add_SimpleApiServicer_to_server(SimpleApiServicer(), server)
#     api_pb2_grpc.add_SquareRootApiServicer_to_server(SquareRootApiServicer(), server)
#
#     server.add_insecure_port('[::]:50051')
#     server.start()
#     print('Server started. Listening on port 50051.')
#     try:
#         while True:
#             time.sleep(60 * 60 * 24)  # 1 day
#     except KeyboardInterrupt:
#         server.stop(0)
#
# if __name__ == '__main__':
#     serve()
#
#

#
#
# assert os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", ""), \
#     f"Please set GOOGLE_APPLICATION_CREDENTIALS env var"
#
# logging.info(f"Attempting to reach API Gateway @ {HOST} using JWT")
#
# with open(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")) as f:
#     sa_info = json.load(f)
#
# logging.debug(sa_info)
# with grpc.secure_channel(HOST, grpc.ssl_channel_credentials()) as channel:
#
#     #stub = pb2_grpc.SimpleApiStub(channel)
#     stub = simple_api_pb2_grpc.SimpleApiStub(channel)
#
#     signed_jwt = generate_jwt(
#         sa_info,
#         audience="your_audience_here"
#     )
#     logging.debug(f"Signed JSON Web Token: {signed_jwt} decoded as a UTF-8 string: {signed_jwt.decode('utf-8')}")
#     metadata = [
#         ("authorization", f"Bearer {signed_jwt.decode('utf-8')}"),
#     ]
#     if FLAGS.api_key:
#         metadata.append(("x-api-key", FLAGS.api_key))
#
#     request = pb2.GreetRequest(name="John")
#     response = stub.Greet(
#         request=request,
#         metadata=metadata
#     )
#     logging.info(response)