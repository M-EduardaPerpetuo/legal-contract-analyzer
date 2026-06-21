# Referência Técnica

Esta seção detalha os componentes críticos que garantem a performance e segurança da solução.



### Stack Tecnológica
* **FastAPI:** Escolhido pela sua capacidade de lidar com requisições assíncronas (async/await), essencial para operações de I/O intensivas (como ler arquivos grandes ou esperar respostas da API de IA).
* **Gestão de Dependências:** O projeto utiliza ambientes virtuais (venv) para isolar bibliotecas de processamento como `python-docx` e `PyPDF2`, garantindo que a execução em produção seja idêntica ao desenvolvimento.

### Segurança e Escalabilidade
* **Desacoplamento:** O uso do n8n como orquestrador permite que a lógica de negócio (Análise Jurídica) fique independente da infraestrutura de notificação (E-mail/Slack/WhatsApp).
* **Tratamento de Erros:** Todas as chamadas para a API externa são encapsuladas em blocos `try/except` para garantir que erros de timeout ou modelos indisponíveis não causem o colapso do servidor, retornando sempre uma mensagem de erro compreensível ao usuário final.