FROM python:3.9-slim-buster

# Install gRPC
RUN python -m pip install grpcio grpcio-tools

# Copy the service code and generated protobuf files into the container
WORKDIR /app
COPY simple_api_pb2.py simple_api_pb2_grpc.py server.py ./

ENV PYTHONUNBUFFERED True
# Expose the gRPC server port
#EXPOSE 50051

## Start the gRPC server
#CMD [ "python", "server.py" ]
CMD ["sh", "-c", "python server.py"]
