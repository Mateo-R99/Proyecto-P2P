"""
Package proto: contiene definiciones .proto y stubs generados de gRPC.
"""

try:
    import transfer_pb2
    import transfer_pb2_grpc
except ImportError:
    # Los stubs se generan con grpcio-tools
    pass
