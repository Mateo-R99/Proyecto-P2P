# 📌 Proyecto P2P

## ✅ Requisitos

* Python 3.10+
* Docker & docker-compose
* Instalar dependencias:

  ```bash
  pip install -r src/requirements.txt
  ```

---

## ⚡ Generar stubs gRPC

Cada vez que modifiques `transfer.proto`, debes regenerar los stubs de Python:

```bash
python -m grpc_tools.protoc -I=src/peer/proto --python_out=src/peer --grpc_python_out=src/peer src/peer/proto/transfer.proto
```

---

## ▶️ Ejecutar en local (sin Docker)

### 1. Crear configuración de peers

Ejemplos en `example_configs/`:

* **peer1.json**
* **peer2.json**
* **peer3.json**

Cada peer tiene:

```json
{
  "ip": "0.0.0.0",
  "rest_port": 8001,
  "grpc_port": 50051,
  "directory": "example_configs/shared1",
  "peer_titular": "http://127.0.0.1:8002",
  "peer_suplente": "http://127.0.0.1:8003"
}
```

📂 Además, cada peer debe tener su carpeta compartida (`shared1/`, `shared2/`, `shared3/`) con algunos archivos iniciales.

---

### 2. Levantar un peer

Ejemplo (para Peer1):

```bash
python src/peer/main.py --config example_configs/peer1.json
```

Levanta el servidor **REST (FastAPI)** y el servidor **gRPC** en paralelo.
Haz lo mismo en otras terminales para Peer2 y Peer3 (ajustando sus configs).

---

### 3. Probar endpoints REST

* Ver archivos de Peer1:

  ```bash
  curl http://127.0.0.1:8001/listado
  ```
* Buscar archivo en Peer1:

  ```bash
  curl "http://127.0.0.1:8001/buscar?archivo=documento1.txt"
  ```
* Buscar archivo en toda la red (Peer1 preguntará a sus vecinos):

  ```bash
  curl "http://127.0.0.1:8001/buscar_en_red?archivo=documento3.txt"
  ```

---

## 🔽/🔼 Pruebas gRPC

### Descargar directamente

```python
from grpc_client import grpc_download
print(grpc_download("127.0.0.1:50053", "documento3.txt"))
```

Guarda el archivo en la carpeta `downloads/`.

### Subir directamente

```python
from grpc_client import grpc_upload
print(grpc_upload("127.0.0.1:50052", "nuevo.txt"))
```

El archivo se guarda en la carpeta compartida del peer (`shared2/` en este ejemplo).

---

## 🧪 Script de pruebas (`test_client.py`)

Hemos agregado un script para facilitar las pruebas de **upload y download**.

Ejecuta:

```bash
python src/peer/test_client.py
```

Ejemplo de salida:

```
=== 🔼 Probando UPLOAD a Peer2 ===
{'ok': True, 'message': 'Archivo recibido en example_configs/shared2\\nuevo.txt'}

=== 🔽 Probando DOWNLOAD desde Peer2 ===
{'ok': True, 'message': 'Archivo guardado en downloads\\nuevo.txt'}

=== 🔽 Probando DOWNLOAD desde Peer3 (ejemplo documento3.txt) ===
{'ok': True, 'message': 'Archivo guardado en downloads\\documento3.txt'}
```

---

## 🚀 Ejecutar con Docker Compose

1. Ajusta `example_configs/peerX.json` y coloca archivos en `example_configs/sharedX/`.
2. Construir y levantar:

   ```bash
   docker-compose up --build
   ```
3. Probar:

   ```bash
   curl http://localhost:8001/listado
   curl "http://localhost:8001/buscar_en_red?archivo=documento3.txt"
   ```

---

## 📂 Estructura del proyecto

```
p2p-project/
├─ src/
│  ├─ peer/
│  │  ├─ main.py              # Servidor principal (FastAPI + gRPC)
│  │  ├─ grpc_server.py       # Servidor gRPC (Upload/Download)
│  │  ├─ grpc_client.py       # Cliente gRPC (Upload/Download)
│  │  ├─ proto/
│  │  │  ├─ transfer.proto    # Definición de servicios gRPC
│  │  ├─ config_loader.py     # Carga de configuración JSON
│  │  ├─ file_index.py        # Listado de archivos
│  │  ├─ client_rest.py       # Cliente REST para buscar en otros peers
│  │  ├─ test_client.py       # Script de pruebas gRPC
│  └─ requirements.txt
├─ example_configs/
│  ├─ peer1.json
│  ├─ peer2.json
│  ├─ peer3.json
│  ├─ shared1/
│  ├─ shared2/
│  ├─ shared3/
├─ docker-compose.yml
└─ README.md
```
