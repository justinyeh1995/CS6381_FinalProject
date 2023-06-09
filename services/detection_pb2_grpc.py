# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import detection_pb2 as detection__pb2


class DetectionServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CheckStatus = channel.unary_unary(
                '/services.DetectionService/CheckStatus',
                request_serializer=detection__pb2.Request.SerializeToString,
                response_deserializer=detection__pb2.Response.FromString,
                )


class DetectionServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CheckStatus(self, request, context):
        """A simple RPC.

        Obtains the status of the given IP address.

        Returns the status of the IP address. If the IP address is not in the
        database, returns false.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DetectionServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CheckStatus': grpc.unary_unary_rpc_method_handler(
                    servicer.CheckStatus,
                    request_deserializer=detection__pb2.Request.FromString,
                    response_serializer=detection__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'services.DetectionService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class DetectionService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CheckStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/services.DetectionService/CheckStatus',
            detection__pb2.Request.SerializeToString,
            detection__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
