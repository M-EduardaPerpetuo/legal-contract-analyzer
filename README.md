# Legal Contract Analyzer 

Enterprise-grade AI pipeline for legal contract analysis and summarization. This system acts as a smart filter for legal departments, reading complex NDA documents and generating structured risk reports with a strict **Human-in-the-Loop** approval gate.

## Architecture Design

The system is built on a microservices architecture, decoupling the orchestration layer from the heavy cognitive processing. This ensures scalability, security, and easy maintenance.

### System Flow
1. **Trigger:** A contract (PDF) is uploaded via Webhook or Email.
2. **Orchestration (n8n):** The workflow engine receives the payload and dispatches it to the processing API.
3. **Cognitive Core (Python/FastAPI):** Parses the binary data, chunks the text, and interacts with the LLM using strict Pydantic schemas.
4. **Human-in-the-Loop (Approval Gate):** The summarized report is sent to a human reviewer (via Slack/Telegram) with `Approve` or `Reject` actions. No final action is taken without human validation.

### Sequence Diagram

```plantuml
@startuml
skinparam handwritten false
skinparam monochrome true
skinparam packageStyle rectangle
skinparam shadowing false

actor "Webhook / Trigger" as User
participant "n8n (Orchestrator)" as n8n
participant "FastAPI (Cognitive Core)" as API
database "LLM (Claude/GPT)" as LLM
actor "Legal Reviewer" as Human

User -> n8n : Upload Contract (PDF)
activate n8n

n8n -> API : POST /api/v1/analyze
activate API

API -> API : Parse PDF & Chunk Text
API -> LLM : Request Analysis (Strict Prompt)
activate LLM

LLM --> API : Structured JSON (Risks, Summary)
deactivate LLM

API --> n8n : Return Validated Payload (Pydantic)
deactivate API

n8n -> Human : Send Report to Slack/Teams\n[Approve] / [Reject]
activate Human

Human --> n8n : Clicks "Approve"
deactivate Human

n8n -> User : Deliver Final Approved Analysis
deactivate n8n
@enduml
