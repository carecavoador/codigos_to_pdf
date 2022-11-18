"""
Este script gera um arquivo PDF com os códigos passados pelo usuário.
"""
import io
import pathlib
import datetime

import PyPDF2

from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics


def divide_em_colunas(lista: list, colunas: int) -> list[list]:
    """
    Divide uma lista em um determinado numero de colulas e retorna
    uma lista contendo uma lista para cada coluna.
    Descaradamente roubado do Stack Overflow:
    https://stackoverflow.com/questions/2130016/
    """
    k, m = divmod(len(lista), colunas)
    return list((lista[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(colunas)))


EMAIL = "837708;837708;837708;837708;837708;837719;837719;837719;837719;"\
        "837719;837724;837724;837724;837724;837726;837726;837726;837726;"\
        "837728;837728;837728;837728;837730;837730;837730;837730;837730;"\
        "837730;837730;837730;837738;837738;837738;837738;837738;837738;"\
        "837740;837740;837740;837740;837742;837742;837742;837742;837750;"\
        "837750;837750;837750;837787;837755;837755;837755;837755;837755;"\
        "837757;837757;837757;837757;837757;837759;837759;837759;837759;"\
        "837759;837767;837767;837767;837775;837775;837775;837775;837779;"\
        "837779;837779;837779;837792;837792;837792;837792;837794;837794;"\
        "837794;837794;837796;837796;837796;837796;"

# Cria uma lista com o valores (string) usando o caractere ';' como separador
numeros = EMAIL.split(";")

# Divide a lista de numeros em 4 colunas
QT_COLUNAS = 4
numeros = divide_em_colunas(numeros, QT_COLUNAS)

# Inicializa um novo buffer de bytes para armazenar o conteudo do novo pdf
bytes_pdf = io.BytesIO()

# Define o tamanho da pagina
documento = canvas.Canvas(bytes_pdf, pagesize=A4)

# Configura a fonte (só fontes Post Script)
TAM_FONTE = 14
FONTE = "Helvetica"

# Desenha o texto na pagina
LARGURA, ALTURA = A4
MARGEM = 20 * mm

# Variável para armazenar a posição horizontal do cursor de texto
pos_X = MARGEM

# Adiciona a lista de códigos dentro do box de texto
for coluna in numeros:

    # Cria um novo box de texto
    texto = documento.beginText()
    texto.setTextOrigin(pos_X, ALTURA - MARGEM - TAM_FONTE)
    texto.setFont(FONTE, TAM_FONTE)

    # Variável para armazenar a largura do maior texto em pontos
    maior_texto = 0.0

    for codigo in coluna:
        # textLine() adiciona uma nova linha de texto
        texto.textLine(codigo)

        # Calcula a largura do texto em pontos
        larg_texto = pdfmetrics.stringWidth(codigo, FONTE, TAM_FONTE)

        maior_texto = max(maior_texto, larg_texto)

    # Acrescenta o box de texto ao documento
    documento.drawText(texto)

    # Ao final de cada coluna, muda a posição X do ponteiro de texto
    pos_X += maior_texto + MARGEM
    texto.setTextOrigin(pos_X, ALTURA - MARGEM - TAM_FONTE)


# Salva o documento
documento.save()

# Salva o novo PDF
# Muda a posição do ponteiro para zero (início do buffer)
bytes_pdf.seek(0)

# Inicializa um objeto PdfReader com o conteúdo do buffer
novo_pdf = PyPDF2.PdfReader(bytes_pdf)

# Inicializa um objeto do tipo writer para gravar o conteúdo do pdf em arquivo
pdf_writer = PyPDF2.PdfWriter()

# Adiciona a página ao gravador
pdf_writer.addPage(novo_pdf.getPage(0))

# Cria o nome do arquivo a ser salvo no Desktop do usuário
desktop = pathlib.Path().home().joinpath("Desktop")
agora = datetime.datetime.now()
nome_arquivo = f"codigos_{agora:%H_%M_%S}"
arquivo_pdf = desktop.joinpath(f"{nome_arquivo}.pdf")

# Escreve os dados em bytes no arquivo .pdf
with open(arquivo_pdf, "wb") as arquivo:
    pdf_writer.write(arquivo)
