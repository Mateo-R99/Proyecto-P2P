import subprocess
import time
import os

PEER_CONFIGS = [
    "example_configs/peer1.json",
    "example_configs/peer2.json",
    "example_configs/peer3.json"
]

processes = []

def start_peers():
    for cfg in PEER_CONFIGS:
        print(f"🚀 Iniciando peer con config: {cfg}")
        p = subprocess.Popen(["python", "src/peer/main.py", "--config", cfg])
        processes.append(p)
        time.sleep(2)  # pequeña pausa para que cada peer arranque bien

if __name__ == "__main__":
    try:
        start_peers()
        print("✅ Todos los peers fueron iniciados por el maestro.")
        print("Puedes probar con: curl http://127.0.0.1:8001/listado")
        # Mantener el proceso maestro vivo
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo peers...")
        for p in processes:
            p.terminate()
