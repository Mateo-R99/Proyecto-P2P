from pathlib import Path
from typing import List

def list_files(directory: str) -> List[dict]:
    p = Path(directory)
    p.mkdir(parents=True, exist_ok=True)  # crea la carpeta si no existe
    files = []
    for f in p.iterdir():
        if f.is_file():
            files.append({
                "name": f.name,
                "size": f.stat().st_size,
                "uri": f"file://{str(f.resolve())}"
            })
    return files

def has_file(directory: str, filename: str) -> bool:
    """
    Verifica si un archivo existe en el directorio, 
    ignorando mayúsculas, minúsculas y espacios extra.
    """
    filename_normalized = filename.strip().lower()
    for f in Path(directory).iterdir():
        if f.is_file():
            if f.name.strip().lower() == filename_normalized:
                return True
    return False
