# Arquitetura do Sistema

O Sistema de Auditoria de Contratos (S.A.C.) foi desenhado para ser uma arquitetura desacoplada e escalável. Abaixo, detalhamos o fluxo de processamento de dados.



### Fluxo de Execução
1. **Ingestão:** O usuário realiza o upload do documento via interface web, que utiliza o protocolo Multipart-form-data para encapsular o binário.
2. **Orquestração (n8n):** O Webhook do n8n atua como o entry-point, validando a integridade do binário e encaminhando a requisição via HTTP Request.
3. **Back-end de Processamento (FastAPI):** O servidor atua como um roteador inteligente:
   - Identifica o MimeType do arquivo (.docx, .pdf, .xlsx).
   - Realiza a normalização e extração de texto bruto.
   - Aplica o encapsulamento do dado para envio via API de IA.
4. **Camada de IA:** O modelo `gemini-2.5-flash` processa o conteúdo extraído contra o nosso prompt de engenharia jurídica, retornando um payload JSON estruturado.
5. **Notificação:** O n8n recebe o JSON e formata um relatório final entregue via e-mail.