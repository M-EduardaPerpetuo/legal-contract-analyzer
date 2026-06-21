from fastapi import FastAPI, UploadFile, File
import pandas as pd
import docx # Nova biblioteca para Word
from PyPDF2 import PdfReader # Nova biblioteca para PDF
import google.generativeai as genai
import io
import json


app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Configuração da Inteligência Artificial
CHAVE_API = "CHAVE"
genai.configure(api_key=CHAVE_API)

model = genai.GenerativeModel('gemini-2.5-flash')

@app.post("/api/v1/analyze")
async def analisar_contrato(file: UploadFile = File(...)):
    try:
        # 2. Lendo o arquivo em bytes e pegando o nome
        conteudo = await file.read()
        nome_arquivo = file.filename.lower()
        texto_contrato = ""

        # 3. Roteador de Arquivos (Descobrindo o que chegou)
        if nome_arquivo.endswith(".xlsx"):
            df = pd.read_excel(io.BytesIO(conteudo))
            texto_contrato = df.to_string()
            
        elif nome_arquivo.endswith(".docx"):
            documento = docx.Document(io.BytesIO(conteudo))
            # Junta todos os parágrafos do Word em um texto só
            texto_contrato = "\n".join([paragrafo.text for paragrafo in documento.paragraphs])
            
        elif nome_arquivo.endswith(".pdf"):
            leitor = PdfReader(io.BytesIO(conteudo))
            # Passa página por página do PDF extraindo o texto
            for pagina in leitor.pages:
                texto_contrato += pagina.extract_text() + "\n"
                
        else:
            # Trava de segurança para formatos desconhecidos
            return {"erro": f"Formato não suportado. Por favor envie .docx, .pdf ou .xlsx. Arquivo recebido: {nome_arquivo}"}

        # 4. Verificação de segurança: O texto está vazio?
        if not texto_contrato.strip():
            return {"erro": "O documento está vazio ou o texto não pôde ser lido (pode ser um PDF feito apenas de imagens)."}

        # 5. Prompt Engineering: Dando as ordens para o Gemini
        prompt = f"""
        Você é um auditor jurídico sênior analisando um contrato. 
        Leia o texto abaixo extraído do documento original.
        
        Avalie o risco das cláusulas e me devolva ESTRITAMENTE um arquivo JSON válido, sem formatação markdown, com a seguinte estrutura:
        {{
            "nivel_de_risco": (número inteiro de 1 a 5, onde 5 é risco altíssimo),
            "resumo_executivo": "Resumo em uma frase dos principais pontos do documento",
            "parecer_sugerido": "Sua recomendação técnica sobre a cláusula mais crítica encontrada"
        }}
        
        Texto do Contrato:
        {texto_contrato}
        """

        # 6. Enviando para o Gemini
        resposta_ia = model.generate_content(prompt)
        texto_resposta = resposta_ia.text.strip()

        # Limpando possíveis formatações (como ```json) que a IA possa colocar
        if texto_resposta.startswith("```json"):
            texto_resposta = texto_resposta[7:-3]
            
        # Transformando a resposta em texto da IA de volta para um objeto JSON real
        dados_json = json.loads(texto_resposta)

        # 7. Devolvendo a resposta real para o n8n
        return dados_json

    except Exception as e:
        return {"erro": f"Erro interno no processamento: {str(e)}"}

