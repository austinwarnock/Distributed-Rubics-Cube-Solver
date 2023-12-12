import rubiks_pb2
import rubiks_pb2_grpc


class RubiksMessagingServer(rubiks_pb2_grpc.SudokuMessagingServicer):
    def __init__(self):
        pass
    
    def getFace