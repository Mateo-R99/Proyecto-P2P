import asyncio
import argparse
import logging
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
from config_loader import load_config
from file_index import list_files, has_file
import client_rest
import grpc_server
import grpc_client

app = FastAPI()
logger = logging.getLogger("peer")

# Configuración global
cfg = None


@app.on_event("startup")
async def startup_event():
    global cfg
    logger.info(f"✅ Peer iniciado con config: {cfg}")


@app.get("/listado")
async def listado():
    try:
        files = list_files(cfg["directory"])
        return JSONResponse(content={"files": files})
    except Exception as e:
        return JSONResponse(content={"error": f"Error listando archivos: {e}"}, status_code=500)


@app.get("/buscar")
async def buscar(archivo: str):
    present = has_file(cfg["directory"], archivo)
    return {"filename": archivo, "present": present, "peer": f"{cfg['ip']}:{cfg['rest_port']}"}


@app.get("/buscar_en_red")
async def buscar_en_red(archivo: str):
    # Revisar local
    if has_file(cfg["directory"], archivo):
        return {"found": True, "peer": f"{cfg['ip']}:{cfg['rest_port']}", "method": "local"}

    # Revisar peers remotos
    for peer_url in (cfg.get("peer_titular"), cfg.get("peer_suplente")):
        if not peer_url:
            continue
        try:
            resp = await client_rest.buscar_archivo(peer_url, archivo)
            if resp.get("present"):
                # Intentar descargar via gRPC desde ese peer
                remote_host = peer_url.replace("http://", "").split(":")[0]
                if remote_host in ("127.0.0.1", "localhost"):
                    remote_host = "127.0.0.1"

                # Ajustar gRPC según el peer remoto
                remote_grpc = None
                if "8001" in peer_url:
                    remote_grpc = "127.0.0.1:50051"
                elif "8002" in peer_url:
                    remote_grpc = "127.0.0.1:50052"
                elif "8003" in peer_url:
                    remote_grpc = "127.0.0.1:50053"

                result = grpc_client.grpc_download(remote_grpc, archivo, output_dir="downloads")

                return {
                    "found": True,
                    "peer": peer_url,
                    "method": "remote_rest+grpc",
                    "download_result": result,
                }
        except Exception as e:
            logger.warning(f"⚠️ Error consultando {peer_url}: {e}")

    return {"found": False}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path to config.json")
    return parser.parse_args()


async def main():
    global cfg
    logging.basicConfig(level=logging.INFO)

    # Leer config desde argumento
    args = parse_args()
    cfg = load_config(args.config)

    # Iniciar gRPC y FastAPI en paralelo
    grpc_task = asyncio.create_task(grpc_server.serve_grpc(cfg))
    rest_task = asyncio.create_task(
        uvicorn.Server(
            uvicorn.Config(app, host=cfg["ip"], port=int(cfg["rest_port"]), log_level="info")
        ).serve()
    )

    await asyncio.gather(grpc_task, rest_task)


if __name__ == "__main__":
    asyncio.run(main())
