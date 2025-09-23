import grpc
import transfer_pb2, transfer_pb2_grpc
import os

CHUNK_SIZE = 1024 * 64  # 64 KB


def grpc_download(peer_address, filename, output_dir="downloads"):
    os.makedirs(output_dir, exist_ok=True)
    dest_path = os.path.join(output_dir, filename)

    with grpc.insecure_channel(peer_address) as channel:
        stub = transfer_pb2_grpc.FileServiceStub(channel)
        req = transfer_pb2.DownloadRequest(filename=filename)

        try:
            with open(dest_path, "wb") as f:
                for resp in stub.Download(req):
                    f.write(resp.chunk)
            return {"ok": True, "message": f"Archivo guardado en {dest_path}"}
        except grpc.RpcError as e:
            return {"ok": False, "message": e.details()}


def grpc_upload(peer_address, filepath):
    def gen():
        filename = os.path.basename(filepath)

        # Primer mensaje: metadata con nombre del archivo
        yield transfer_pb2.UploadRequest(filename=filename)

        # Luego enviar solo los chunks binarios
        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break
                yield transfer_pb2.UploadRequest(chunk=chunk)

    with grpc.insecure_channel(peer_address) as channel:
        stub = transfer_pb2_grpc.FileServiceStub(channel)
        try:
            resp = stub.Upload(gen())
            return {"ok": resp.ok, "message": resp.message}
        except grpc.RpcError as e:
            return {"ok": False, "message": e.details()}
