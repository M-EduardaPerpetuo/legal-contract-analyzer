import google.generativeai as genai

CHAVE_API = "Chave" 
genai.configure(api_key=CHAVE_API)

print("--- BUSCANDO MODELOS DISPONÍVEIS ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
    print("------------------------------------")
except Exception as e:
    print(f"Erro ao buscar modelos: {e}")