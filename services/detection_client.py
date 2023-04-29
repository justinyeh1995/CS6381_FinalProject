from concurrent import futures
import logging

import grpc
import detection_pb2
import detection_pb2_grpc

import csv
import os
import sys
import traceback

class DetectionClient():
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def run(self):
        # Create a gRPC channel + stub.
        channel = grpc.insecure_channel(f'{self.host}:{self.port}')
        stub = detection_pb2_grpc.DetectionServiceStub(channel)

        # Create a request for the server.
        # the request should contain the ip address of the client
        request = detection_pb2.Request(ip_address='129.114.26.225')

        # Make the request synchronously.
        response = stub.CheckStatus(request)

        # Print the response.
        print(response)

def run_client():
    client = DetectionClient('localhost', 50051)
    client.run()    

if __name__ == '__main__':
    run_client()
