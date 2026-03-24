import socket
import threading

HOST = "0.0.0.0"
PORT = 5000


def calcular_area(mensagem: str) -> str:
    try:
        base_str, altura_str = mensagem.strip().split(",")
        base = float(base_str)
        altura = float(altura_str)
        area = (base * altura) / 2
        return f"Área: {area:.2f}"
    except (ValueError, TypeError):
        return "ERRO: entrada inválida"


def tratar_cliente(conn: socket.socket, endereco: tuple[str, int]) -> None:
    with conn:
        try:
            dados = conn.recv(1024)
            if not dados:
                return
            mensagem = dados.decode("utf-8", errors="ignore")
            resposta = calcular_area(mensagem)
            conn.sendall(resposta.encode("utf-8"))
        except Exception:
            conn.sendall("ERRO: entrada inválida".encode("utf-8"))



def iniciar_servidor() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PORT))
        servidor.listen()
        print(f"Servidor TCP escutando em {HOST}:{PORT}")

        while True:
            conn, endereco = servidor.accept()
            thread = threading.Thread(
                target=tratar_cliente,
                args=(conn, endereco),
                daemon=True,
            )
            thread.start()


if __name__ == "__main__":
    iniciar_servidor()
