import json
import logging
from pathlib import Path

logger = logging.getLogger("config_loader")

def load_config(path: str) -> dict:
    """
    Carga la configuración desde el archivo JSON indicado.
    Si el archivo no existe o es inválido, lanza una excepción.
    """
    config_path = Path(path).resolve()
    logger.info(f"📂 Cargando configuración desde: {config_path}")
    
    if not config_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo de configuración: {config_path}")
    
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    # Validar campos obligatorios
    required_fields = ["ip", "rest_port", "grpc_port", "directory"]
    for field in required_fields:
        if field not in config:
            raise KeyError(f"Falta el campo obligatorio '{field}' en {config_path}")
    
    return config
