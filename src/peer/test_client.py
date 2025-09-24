from grpc_client import grpc_upload, grpc_download

def main():
    # Configura aquí la dirección y puerto del peer al que quieres probar
    peer2 = "127.0.0.1:50052"
    peer3 = "127.0.0.1:50053"

    print("=== 🔼 Probando UPLOAD a Peer2 ===")
    result_upload = grpc_upload(peer2, "nuevo.txt")
    print(result_upload)

    print("\n=== 🔽 Probando DOWNLOAD desde Peer2 ===")
    result_download = grpc_download(peer2, "nuevo.txt")
    print(result_download)

    print("\n=== 🔽 Probando DOWNLOAD desde Peer3 (ejemplo documento3.txt) ===")
    result_download_peer3 = grpc_download(peer3, "documento3.txt")
    print(result_download_peer3)


if __name__ == "__main__":
    main()
