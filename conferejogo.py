from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

def conectar_banco():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="danbina21",
        database="megasena"
    )

@app.route("/")
def index():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, numeros FROM jogos")
    jogos = cursor.fetchall()
    conexao.close()
    return render_template("index.html", jogos=jogos)

@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        numeros = request.form["numeros"]

        conexao = conectar_banco()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO jogos (numeros) VALUES (%s)", (numeros,))
        conexao.commit()
        conexao.close()

        return redirect(url_for("index"))

    return render_template("cadastrar.html")

@app.route("/deletar/<int:id>")
def deletar(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM jogos WHERE id = %s", (id,))
    conexao.commit()
    conexao.close()
    return redirect(url_for("index"))

@app.route("/verificar", methods=["GET", "POST"])

def verificar():
    resultados = []
    erro = None  # Variável para armazenar a mensagem de erro

    if request.method == "POST":
        sorteados = request.form["sorteados"]

        try:
            
            # Divide a string pela vírgula e converte cada valor para int
            numeros_sorteados = [int(n.strip()) for n in sorteados.split(",")]

            # Verifica Quantidade de números
            if len(numeros_sorteados) != 6:
                raise ValueError("Erro: insira 6 números válidos entre 1 e 60 separados por vírgula.")
            
            # Verifica se está entre 1 e 60
            for n in numeros_sorteados:
                if n < 1 or n > 60:
                    raise ValueError("Erro: insira 6 números válidos entre 1 e 60 separados por vírgula.")

            # Se os números forem válidos, consulta os jogos cadastrados no banco
            conexao = conectar_banco()
            cursor = conexao.cursor()
            cursor.execute("SELECT id, numeros FROM jogos")
            jogos = cursor.fetchall()
            conexao.close()

            # Verifica os acertos nos jogos
            for jogo in jogos:
                id_jogo, numeros = jogo
                numeros_jogo = list(map(int, numeros.split()))
                acertos = len(set(numeros_jogo) & set(numeros_sorteados))

                if acertos == 6:
                    status = "SENA - Você está milionário"
                elif acertos == 5:
                    status = "QUINA - Você ganhou uma boa grana"
                elif acertos == 4:
                    status = "QUADRA - Você ganhou um trocado"
                else:
                    status = f"{acertos} acertos"

                resultados.append((id_jogo, numeros_jogo, status))

        except ValueError as e:
            # Se ocorrer algum erro, armazenamos a mensagem de erro
            erro = str(e)
            resultados = []

    return render_template("verificar.html", resultados=resultados, erro=erro)



if __name__ == "__main__":
    app.run(debug=True)
