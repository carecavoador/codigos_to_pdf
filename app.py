"""
Este script gera um arquivo PDF com os códigos passados pelo usuário.
"""
import io
import pathlib
import datetime
import argparse

import PyPDF2

from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4, A3, LETTER
from reportlab.pdfbase import pdfmetrics


tamanhos = {
    "a4": A4,
    "a3": A3,
    "carta": LETTER
}

parser = argparse.ArgumentParser()
parser.add_argument(
    "codigos",
    help="o texto contendo os códigos separados",
    type=str,
    nargs="?" # argumento posicional opcional
)
parser.add_argument(
    "-s", "--separador",
    help="o caractere que separa os códigos",
    type=str,
    default=";"
)
parser.add_argument(
    "-n", "--colunas",
    help="o número de colunas desejado",
    type=int,
    default=4
)
parser.add_argument(
    "-p", "--tamanho-pagina",
    help="o tamanho de página desejado",
    type=str,
    default="A4"
)
parser.add_argument(
    "-m", "--margem",
    help="define o tamanho da margem em milímetros",
    type=int,
    default=20
)
parser.add_argument(
    "-f", "--fonte",
    help="nome da fonte (post script) para ser utilizada nos códigos",
    type=str,
    default="Helvetica"
)
parser.add_argument(
    "-t", "--tamanho-fonte",
    help="tamanho da fonte em pontos",
    type=int,
    default=14
)
parser.add_argument(
    "arquivo",
    help="o nome do arquivo PDF de saída",
    nargs="?"
)

args = parser.parse_args()

def divide_em_colunas(lista: list, colunas: int) -> list[list]:
    """
    Divide uma lista em um determinado numero de colulas e retorna
    uma lista contendo uma lista para cada coluna.
    Descaradamente roubado do Stack Overflow:
    https://stackoverflow.com/questions/2130016/
    """
    k, m = divmod(len(lista), colunas)
    return list((lista[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(colunas)))


def main() -> None:
    if args.codigos:
        codigos = args.codigos
    else:
        codigos = input("> Insira os códigos: ")

    codigos = codigos.split(args.separador)
    lista_colunas = divide_em_colunas(codigos, args.colunas)
    bytes_pdf = io.BytesIO()
    tamanho_pagina = tamanhos[args.tamanho_pagina.lower()]
    _, altura = tamanho_pagina
    margem = args.margem * mm
    margem_topo = 20 * mm
    margem_lateral = 20 * mm
    documento = canvas.Canvas(bytes_pdf, pagesize=tamanho_pagina)
    fonte = args.fonte
    tam_fonte = args.tamanho_fonte

    pos_x = margem_lateral

    for coluna in lista_colunas:
        texto = documento.beginText()
        texto.setTextOrigin(pos_x, altura - margem_topo - tam_fonte)
        texto.setFont(fonte, tam_fonte)
        maior_texto = 0.0
        for codigo in coluna:
            texto.textLine(codigo)
            larg_texto = pdfmetrics.stringWidth(codigo, fonte, tam_fonte)
            maior_texto = max(maior_texto, larg_texto)
        documento.drawText(texto)
        pos_x += maior_texto + margem
        texto.setTextOrigin(pos_x, altura - margem_topo - tam_fonte)
    documento.save()
    bytes_pdf.seek(0)
    novo_pdf = PyPDF2.PdfReader(bytes_pdf)
    pdf_writer = PyPDF2.PdfWriter()
    pdf_writer.addPage(novo_pdf.getPage(0))
    desktop = pathlib.Path().home().joinpath("Desktop")
    agora = datetime.datetime.now()
    if args.arquivo:
        nome_arquivo = args.arquivo
    else:
        nome_arquivo = f"codigos_{agora:%H_%M_%S}"
    arquivo_pdf = desktop.joinpath(f"{nome_arquivo}.pdf")
    with open(arquivo_pdf, "wb") as arquivo:
        pdf_writer.write(arquivo)


if __name__ == "__main__":
    main()
