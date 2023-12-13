import rubiks_pb2
import rubiks_pb2_grpc
import grpc
import socket
from concurrent import futures
from cube import Face, COLOR_MAP

global face


class RubiksMessagingServer(rubiks_pb2_grpc.RubiksMessagingServicer):    
    def GetColumn(self, request, context):
        print("Received request for column: " + str(request.column))
        col = face.get_column(request.column)
        return rubiks_pb2.SquareTriple(index = request.index, square1 = col[0], square2 = col[1], square3 = col[2])
    
    def GetRow(self, request, context):
        print("Received request for row: " + str(request.row))
        row = face.get_row(request.row)
        return rubiks_pb2.SquareTriple(index = request.index, square1 = row[0], square2 = row[1], square3 = row[2])
    
    def SetColumn(self, request, context):
        print("Received request to set column: " + str(request.column))
        face.set_column(request.column, [request.square1, request.square2, request.square3])
        return rubiks_pb2.Ack(status = "OK")
    
    def SetRow(self, request, context):
        print("Received request to set row: " + str(request.row))
        face.set_row(request.row, [request.square1, request.square2, request.square3])
        return rubiks_pb2.Ack(status = "OK")
    
    def Rotate(self, request, context):
        print("Received request to rotate: " + str(request.direction))
        face.rotate(request.direction)
        return rubiks_pb2.Ack(status = "OK")

def server(HOST,PORT):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rubiks_pb2_grpc.add_RubiksMessagingServicer_to_server(RubiksMessagingServer(), server)
    server.add_insecure_port(HOST + ':' + PORT)
    server.start()
    server.wait_for_termination()
    
def client(HOST, PORT):
    channel = grpc.insecure_channel(HOST + ':' + PORT)
    stub = rubiks_pb2_grpc.RubiksMessagingStub(channel)
    response = stub.GetColumn(rubiks_pb2.Index(index = 0))
    print(response.square1, response.square2, response.square3)
    

if __name__ == '__main__':
    HOST = socket.gethostname()
    PORT = 50051
    
    if HOST != 'result':
        PORT = format(ord(HOST), '02d')
        print(PORT)
        server(HOST, str(PORT))
    else:
        pass
        #client()
        