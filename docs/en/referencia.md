# Technical Reference

This section details the critical components that ensure the solution's performance and security.

### Technology Stack
* **FastAPI:** Chosen for its ability to handle asynchronous requests (async/await), which is essential for I/O-intensive operations (such as reading large files or waiting for AI API responses).
* **Dependency Management:** The project uses virtual environments (venv) to isolate processing libraries like `python-docx` and `PyPDF2`, ensuring that production execution is identical to development.

### Security and Scalability
* **Decoupling:** Using n8n as an orchestrator allows the business logic (Legal Analysis) to remain independent of the notification infrastructure (Email/Slack/WhatsApp).
* **Error Handling:** All external API calls are wrapped in `try/except` blocks to ensure that timeout errors or unavailable models do not cause server crashes, always returning a clear error message to the end user.