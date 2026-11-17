
from pathlib import Path


# Diretórios
BASE_DIR = Path(__file__).parent

PLANILHA = BASE_DIR / "dados" / "leads.xlsx"

PASTA_ARQUIVOS = BASE_DIR / "arquivos"

RELATORIO = BASE_DIR / "relatorios" / "envios.csv"


# Arquivo que será enviado
ARQUIVO_ENVIO = (
    PASTA_ARQUIVOS / "BRdata Boutiques.pdf"
)


# Mensagem personalizada
MENSAGEM = """
Olá! Tudo bem? Eu sou o Gabriel! 😊

A empresa *{nome}* já conhece a BRdata?

Somos especialistas em soluções de gestão e já atendemos empresas como *Flaboutique, M.Max, Taty Modas, Latitude, Doce Idade e Moda Morena*!

Nosso sistema simplifica a gestão da sua loja, reunindo vendas, estoque, financeiro e emissão fiscal, além de oferecer integração com TEF e dashboards gerenciais para acompanhar os resultados do seu negócio.

🚀 Que tal conhecer nossa solução e descobrir como podemos ajudar a *{nome}* a crescer ainda mais?

Podemos agendar uma demonstração sem compromisso!

📲 Vamos conversar?
"""


# Colunas da planilha
COLUNA_NOME = "nome"

COLUNA_TELEFONE = "telefone"


# País: Brasil
DDI_PADRAO = "55"
