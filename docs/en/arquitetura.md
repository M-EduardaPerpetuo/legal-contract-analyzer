# System Architecture

The Legal Contract Audit System (S.A.C. - Sistema de Auditoria de Contratos) is designed with a decoupled and scalable architecture. Below, we detail the data processing flow.

### Execution Flow
1. **Ingestion:** The user uploads the document via the web interface, which uses the Multipart-form-data protocol to encapsulate the binary file.
2. **Orchestration (n8n):** The n8n Webhook acts as the entry point, validating the binary's integrity and forwarding the request via HTTP Request.
3. **Processing Back-end (FastAPI):** The server acts as a smart router:
   - Identifies the file's MimeType (.docx, .pdf, .xlsx).
   - Performs normalization and raw text extraction.
   - Encapsulates the data for transmission via the AI API.
4. **AI Layer:** The `gemini-2.5-flash` model processes the extracted content against our legal engineering prompt, returning a structured JSON payload.
5. **Notification:** n8n receives the JSON and formats a final report delivered via email.