import grpc
import earthquake_pb2
import earthquake_pb2_grpc

def run():
    # Connect to the gRPC server (Replace localhost with Instance 1's Public IP if running remotely)
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = earthquake_pb2_grpc.EarthquakeServiceStub(channel)
        print("Querying the Web Service for the latest data...")
        response = stub.GetLatestEarthquake(earthquake_pb2.Empty())
        
        if response.location == "None":
            print("No significant earthquakes recorded yet.")
        else:
            print(f"🚨 LATEST ALERT: Magnitude {response.magnitude} in {response.location}")

if __name__ == '__main__':
    run()