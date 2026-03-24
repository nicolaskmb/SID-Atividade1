import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.util.Locale;
import java.util.Scanner;

public class ClienteTCP {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);

        try (Scanner scanner = new Scanner(System.in)) {
            System.out.print("Digite a base: ");
            double base = scanner.nextDouble();

            System.out.print("Digite a altura: ");
            double altura = scanner.nextDouble();

            String payload = base + "," + altura;

            try (
                Socket socket = new Socket("localhost", 5000);
                PrintWriter writer = new PrintWriter(socket.getOutputStream(), true, StandardCharsets.UTF_8);
                BufferedReader reader = new BufferedReader(
                    new InputStreamReader(socket.getInputStream(), StandardCharsets.UTF_8)
                )
            ) {
                writer.println(payload);
                String resposta = reader.readLine();

                if (resposta != null) {
                    System.out.println("Resposta do servidor: " + resposta);
                } else {
                    System.out.println("O servidor encerrou a conexão sem resposta.");
                }
            }
        } catch (IOException e) {
            System.err.println("Erro de comunicação com o servidor: " + e.getMessage());
        } catch (Exception e) {
            System.err.println("Erro ao ler entrada do usuário: " + e.getMessage());
        }
    }
}
