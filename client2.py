import argparse
import os
import json
import logging

import grpc

import simple_api_pb2 as pb2
import simple_api_pb2_grpc as pb2_grpc
#from get_jwt import generate_jwt

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)


def main(FLAGS):

    #PORT = FLAGS.port
    HOST = FLAGS.host

    if HOST == "localhost":
        with grpc.insecure_channel(f"{HOST}:{PORT}") as channel:
            stub = pb2_grpc.SimpleApiStub(channel)

            request = pb2.GreetRequest(name="John")
            response = stub.Greet(request)
            logging.info(response)
    else:
        if not FLAGS.use_jwt:
            logging.info(f"Attempting to connect to {HOST}")
            with grpc.secure_channel(HOST, grpc.ssl_channel_credentials()) as channel:
                stub = pb2_grpc.SimpleApiStub(channel)
                request = pb2.GreetRequest(name="John")
                response = stub.Greet(
                    request=request,
                    metadata=(("x-api-key", FLAGS.api_key),)
                )
                logging.info(response)
        else:
            assert os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", ""), \
                f"Please set GOOGLE_APPLICATION_CREDENTIALS env var"

            logging.info(f"Attempting to reach API Gateway @ {HOST} using JWT")

            with open(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")) as f:
                sa_info = json.load(f)

            logging.debug(sa_info)
            with grpc.secure_channel(HOST, grpc.ssl_channel_credentials()) as channel:

                stub = pb2_grpc.SimpleApiStub(channel)

                signed_jwt = generate_jwt(
                    sa_info,
                    audience="your_audience_here"
                )
                logging.debug(f"Signed JSON Web Token: {signed_jwt} decoded as a UTF-8 string: {signed_jwt.decode('utf-8')}")
                metadata = [
                    ("authorization", f"Bearer {signed_jwt.decode('utf-8')}"),
                ]
                if FLAGS.api_key:
                    metadata.append(("x-api-key", FLAGS.api_key))

                request = pb2.GreetRequest(name="John")
                response = stub.Greet(
                    request=request,
                    metadata=metadata
                )
                logging.info(response)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "host",
        type=str,
        default="localhost",
        help="Hostname of the API Gateway"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Port number of the API Gateway, only used for localhost"
    )
    parser.add_argument(
        "--use_jwt",
        action="store_true",
        help="Use JWT to authenticate to API Gateway"
    )
    parser.add_argument(
        "--api_key",
        type=str,
        help="API Key for the API Gateway"
    )
    FLAGS, unparsed = parser.parse_known_args()
    if unparsed:
        logging.warning("Unparsed arguments: {}".format(unparsed))

    logging.debug("Arguments: {}".format(FLAGS))
    main(FLAGS)
