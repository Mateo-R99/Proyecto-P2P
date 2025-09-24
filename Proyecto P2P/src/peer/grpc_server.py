import grpc
import asyncio
import os
import logging
import transfer_pb2, transfer_pb2_grpc

logger = logging.getLogger("grpc_server")

CHUNK_SIZE = 1024 * 64

class FileServiceServicer(transfer_pb2_grpc.FileServiceServicer):
    def __init__(self, cfg):
        self.cfg = cfg

    async def Download(self, request, context):
        file_path = os.path.join(self.cfg["directory"], request.filename)
        if not os.path.exists(file_path):
            await context.abort(grpc.StatusCode.NOT_FOUND, "Archivo no encontrado")

        logger.info(f"[gRPC] 📤 Enviando {file_path}")
        with open(file_path, "rb") as f:
            while chunk := f.read(CHUNK_SIZE):
                yield transfer_pb2.DownloadResponse(chunk=chunk)

    def Upload(self, request_iterator, context):
        try:
            filename, filepath, f = None, None, None
            os.makedirs(self.cfg["directory"], exist_ok=True)

            for req in request_iterator:
                if req.filename:
                    filename = req.filename
                    filepath = os.path.join(self.cfg["directory"], filename)
                    f = open(filepath, "wb")
                if req.chunk and f:
                    f.write(req.chunk)

            if f:
                f.close()

            return transfer_pb2.UploadResponse(ok=True, message=f"Archivo recibido en {filepath}")
        except Exception as e:
            logger.error(f"Error en Upload: {e}")
            return transfer_pb2.UploadResponse(ok=False, message=str(e))


# 🔑 Agregar esta función al final
async def serve_grpc(cfg):
    server = grpc.aio.server()
    transfer_pb2_grpc.add_FileServiceServicer_to_server(FileServiceServicer(cfg), server)
    server.add_insecure_port(f"0.0.0.0:{cfg['grpc_port']}")
    logger.info(f"[gRPC] ✅ Servidor escuchando en 0.0.0.0:{cfg['grpc_port']}")
    await server.start()
    await server.wait_for_termination()
