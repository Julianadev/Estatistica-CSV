import random
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QTextEdit, \
    QFileDialog, QMessageBox

# Função para simular um cenário
def simular_cenario(parametros):
    resultados = []
    for _ in range(parametros['numero_lancamentos']):
        resultado = random.choice(parametros['dados_estatisticos'])
        resultados.append(resultado)
    return resultados

# Função para realizar as simulações
def simular(parametros, numero_cenarios):
    simulacoes = []
    for _ in range(numero_cenarios):
        cenario = simular_cenario(parametros)
        simulacoes.append(cenario)
    return simulacoes


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simulador Estatístico")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()

        self.numero_lancamentos_label = QLabel("Número de Lançamentos:")
        layout.addWidget(self.numero_lancamentos_label)

        self.numero_lancamentos_entry = QTextEdit()
        layout.addWidget(self.numero_lancamentos_entry)

        self.numero_cenarios_label = QLabel("Número de Cenários:")
        layout.addWidget(self.numero_cenarios_label)

        self.numero_cenarios_entry = QTextEdit()
        layout.addWidget(self.numero_cenarios_entry)

        self.dados_estatisticos_label = QLabel("Dados Estatísticos:")
        layout.addWidget(self.dados_estatisticos_label)

        self.dados_estatisticos_entry = QTextEdit()
        layout.addWidget(self.dados_estatisticos_entry)

        self.limpar_button = QPushButton("Limpar Dados")
        self.limpar_button.clicked.connect(self.limpar_dados)
        layout.addWidget(self.limpar_button)

        self.ler_csv_button = QPushButton("Ler Dados de CSV")
        self.ler_csv_button.clicked.connect(self.ler_dados_csv)
        layout.addWidget(self.ler_csv_button)

        self.executar_button = QPushButton("Executar")
        self.executar_button.clicked.connect(self.executar_simulacao)
        layout.addWidget(self.executar_button)

        self.resultado_text = QTextEdit()
        layout.addWidget(self.resultado_text)

        self.salvar_button = QPushButton("Salvar Resultados")
        self.salvar_button.clicked.connect(self.salvar_arquivo)
        layout.addWidget(self.salvar_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def limpar_dados(self):
        self.numero_lancamentos_entry.clear()
        self.numero_cenarios_entry.clear()
        self.dados_estatisticos_entry.clear()
        self.resultado_text.clear()

    def ler_dados_csv(self):
        file_dialog = QFileDialog()
        csv_file, _ = file_dialog.getOpenFileName(self, "Selecionar Arquivo CSV")

        if csv_file:
            with open(csv_file, 'r', encoding='utf-8') as file:
                dados_estatisticos = file.read().splitlines()
            self.dados_estatisticos_entry.setPlainText('\n'.join(dados_estatisticos))

    def executar_simulacao(self):
        numero_lancamentos = int(self.numero_lancamentos_entry.toPlainText())
        dados_estatisticos = self.dados_estatisticos_entry.toPlainText().splitlines()

        if len(dados_estatisticos) == 0:
            QMessageBox.warning(self, "Dados Insuficientes", "Por favor, forneça os dados estatísticos.")
            return

        try:
            numero_cenarios = int(self.numero_cenarios_entry.toPlainText())
        except ValueError:
            QMessageBox.warning(self, "Número de Cenários Inválido", "Por favor, insira um número válido de cenários.")
            return

        parametros = {
            'numero_lancamentos': numero_lancamentos,
            'dados_estatisticos': dados_estatisticos
        }

        simulacoes = simular(parametros, numero_cenarios)

        self.resultado_text.clear()
        for i, cenario in enumerate(simulacoes):
            self.resultado_text.append(f"Cenário {i + 1}:")
            self.resultado_text.append(', '.join(cenario))
            self.resultado_text.append('')

    def salvar_arquivo(self):
        text = self.resultado_text.toPlainText()

        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, "Salvar Resultados", "", "Arquivo de Texto (*.txt)")

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(text)
                QMessageBox.information(self, "Salvar Arquivo", "Os resultados foram salvos com sucesso.")
            except Exception as e:
                QMessageBox.warning(self, "Erro ao Salvar Arquivo", f"Ocorreu um erro ao salvar o arquivo: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
