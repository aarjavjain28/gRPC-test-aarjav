import os
import grpc
import google.auth
from google.oauth2 import credentials as oauth2_credentials
import google.auth.transport.requests
import simple_api_pb2
import simple_api_pb2_grpc
import logging



def run():
    # Authenticate with Google Cloud and obtain the credentials object.
    credentials, project_id = google.auth.default()

    # Obtain an access token using the credentials.
    auth_req = google.auth.transport.requests.Request()
    credentials.refresh(auth_req)
    access_token = credentials.token

    # Create a custom metadata plugin to inject the access token.
    class AccessTokenAuthenticator(grpc.AuthMetadataPlugin):
        def __init__(self, token):
            self._token = token

        def __call__(self, context, callback):
            metadata = (('authorization', f'Bearer {self._token}'),)
            callback(metadata, None)

    auth_plugin = AccessTokenAuthenticator(access_token)
    call_credentials = grpc.metadata_call_credentials(auth_plugin)

    # Create a secure channel using SSL credentials.
    ssl_credentials = grpc.ssl_channel_credentials()

    # Combine the SSL credentials with the metadata call credentials.
    composite_credentials = grpc.composite_channel_credentials(ssl_credentials, call_credentials)

    # Obtain the target URL of the Cloud Run service.
    target_url = 'aarjav-grpc-test-5crxeuc6wq-nw.a.run.app'  # Use your actual Cloud Run service URL.

    # Create a secure gRPC channel using the composite credentials object and target URL.
    channel = grpc.secure_channel(target_url, composite_credentials)

    # Create a stub for the gRPC service.
    stub = simple_api_pb2_grpc.SimpleApiStub(channel)

    # Make the gRPC call to the server.
    response = stub.Greet(simple_api_pb2.GreetRequest(name='World'))

    # Print the response from the server.
    print(response.greeting)

if __name__ == '__main__':
    run()
