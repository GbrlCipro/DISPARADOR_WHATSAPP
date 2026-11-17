import pandas as pd
import urllib.parse
import time
import re
import os
import struct

import win32clipboard
import win32gui
import win32con
import win32api

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import (
    PLANILHA,
    ARQUIVO_ENVIO,
    MENSAGEM,
    COLUNA_NOME,
    COLUNA_TELEFONE,
    DDI_PADRAO
)

driver = None

# ==========================================
# CARREGAR PLANILHA
def carregar_leads():

    print("Carregando planilha...")

    if PLANILHA.suffix.lower() == ".csv":

        df = pd.read_csv(
            PLANILHA,
            dtype=str
        )

    else:

        df = pd.read_excel(
            PLANILHA,
            dtype=str
        )

    df.columns = df.columns.str.strip().str.lower()

    return df.fillna("")
# ==========================================

# ==========================================
# NORMALIZAR TELEFONE
def normalizar_telefone(telefone):

    numero = re.sub(
        r"\D",
        "",
        str(telefone)
    )

    if numero.startswith(DDI_PADRAO):

        pass

    elif len(numero) in (10, 11):

        numero = DDI_PADRAO + numero

    else:

        return None

    if len(numero) not in (12, 13):

        return None

    return numero
# ==========================================

# ==========================================
# COPIAR PDF PARA ÁREA DE TRANSFERÊNCIA
def copiar_arquivo():

    arquivo = os.path.abspath(
        str(ARQUIVO_ENVIO)
    )

    if not os.path.isfile(arquivo):

        raise FileNotFoundError(
            f"Arquivo não encontrado: {arquivo}"
        )

    dados = (
        struct.pack(
            "IiiII",
            20,
            0,
            0,
            0,
            1
        )
        + arquivo.encode("utf-16le")
        + b"\x00\x00\x00\x00"
    )

    win32clipboard.OpenClipboard()

    try:

        win32clipboard.EmptyClipboard()

        win32clipboard.SetClipboardData(
            win32con.CF_HDROP,
            dados
        )

    finally:

        win32clipboard.CloseClipboard()

    print("\nPDF copiado para a área de transferência!")
# ==========================================

# ==========================================
# INICIAR NAVEGADOR
def iniciar_navegador():

    global driver

    options = Options()

    options.add_argument(
        "--user-data-dir=C:/whatsapp_python"
    )

    driver = webdriver.Chrome(options=options)

    driver.get("https://web.whatsapp.com")

    input(
        "\nFaça login no WhatsApp Web e pressione ENTER..."
    )

    # Aguarda o Chrome estabilizar
    time.sleep(1)

    # Recupera a janela do PowerShell
    shell = win32gui.FindWindow(
        "ConsoleWindowClass",
        None
    )

    if shell:

        win32gui.ShowWindow(
            shell,
            win32con.SW_RESTORE
        )

        win32gui.SetForegroundWindow(shell)

    print("\nWhatsApp conectado!")

    # Copia o PDF apenas uma vez
    copiar_arquivo()

    print("\nPDF preparado para todos os envios!")
# ==========================================

# ==========================================
# ABRIR WHATSAPP
def abrir_whatsapp(nome, telefone):

    mensagem = MENSAGEM.format(nome=nome)

    texto = urllib.parse.quote(mensagem)

    url = (
        "https://web.whatsapp.com/send"
        f"?phone={telefone}&text={texto}"
    )

    print(f"\nAbrindo conversa de {nome}...")

    driver.get(url)

    time.sleep(5)

    # Aguarda o campo de mensagem
    campo = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "[data-testid='conversation-compose-box-input']"
        ))
    )

    # Cola o PDF
    campo.send_keys(Keys.CONTROL, "v")

    print("\nPDF colado no WhatsApp!")

    time.sleep(3)

    print("\nConfira o contato, o PDF e a mensagem.")
    print("Clique manualmente em ENVIAR.")
# ==========================================

# ==========================================
# EXECUTAR SISTEMA
def executar():

    iniciar_navegador()

    print("\n=== SISTEMA DE LEADS ===")

    df = carregar_leads()

    print(
        f"Total de leads: {len(df)}"
    )

    for _, linha in df.iterrows():

        nome = str(
            linha[COLUNA_NOME]
        ).strip()

        telefone = normalizar_telefone(
            linha[COLUNA_TELEFONE]
        )

        if not nome or not telefone:

            print(
                "Lead ignorado: dados inválidos."
            )

            continue

        print("\n------------------------")

        print("Nome:", nome)

        print("Telefone:", telefone)

        resposta = input(
            "Abrir conversa? (S/N): "
        ).strip().upper()

        if resposta != "S":

            continue

        try:

            abrir_whatsapp(
                nome,
                telefone
            )

            print("\nConfira o contato e o consentimento.")
            print("Confira o PDF anexado.")
            print("Confira a mensagem personalizada.")
            print("Envie manualmente quando estiver tudo certo.")

            input(
                "\nPressione ENTER para passar ao próximo lead..."
            )

        except Exception as erro:

            print(
                "\nErro ao preparar lead:",
                erro
            )

            input(
                "Pressione ENTER para continuar..."
            )
# ==========================================

# ==========================================
# INICIALIZAÇÃO
if __name__ == "__main__":

    try:

        executar()

    except Exception as erro:

        print(
            "\nERRO:",
            erro
        )

    finally:

        if driver is not None:

            driver.quit()

        input(
            "\nPressione ENTER para fechar..."
        )
# ==========================================

