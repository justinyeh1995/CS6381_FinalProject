## Team 10

from concurrent import futures
import logging

import grpc
import detection_pb2
import detection_pb2_grpc

import db_resources

import csv
import os
import sys
import traceback

class DetectionServer(detection_pb2_grpc.DetectionServiceServicer):
    def __init__(self):
        self.block_list_db = db_resources.read_database()

    # need fix
    def CheckStatus(self, request, context):
        # assume that request.address is the IP address being checked
        # we can perform some logic to determine if the address is valid
        if request.ip_address in self.block_list_db: # query self.db here
            status = True
        else:
            status = False
        
        return detection_pb2.Response(status=status) 


def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    detection_pb2_grpc.add_DetectionServiceServicer_to_server(DetectionServer(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
