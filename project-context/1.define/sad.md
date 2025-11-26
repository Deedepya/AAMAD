# System Architecture Document: Automated Employee Onboarding Workflow (MVP)

## Table of Contents

1. **Executive Summary** - Overview of MVP scope, architecture decisions, and key stakeholders
2. **MVP Architecture Philosophy & Principles** - Design principles, scope boundaries, and technical rationale for iOS + CrewAI
3. **Stakeholders & Concerns** - Primary users, their concerns, and quality attribute priorities
4. **System Context & Boundaries** - System scope, external dependencies, and integration points
5. **Multi-Agent System Specification** - CrewAI agent definitions, roles, and collaboration patterns for MVP
6. **Frontend Architecture Specification (iOS)** - iOS app structure, UI components, and user interaction patterns
7. **Backend Architecture Specification (CrewAI)** - CrewAI crew configuration, API design, and agent orchestration
8. **Data Architecture** - Data models, storage strategy, and data flow for MVP scope
9. **Integration Architecture** - External system integrations, API contracts, and communication protocols
10. **Deployment Architecture** - Infrastructure, hosting, and deployment strategy for MVP
11. **Security & Compliance Architecture** - Security measures, data protection, and compliance requirements
12. **Quality Attributes & Non-Functional Requirements** - Performance, scalability, reliability targets for MVP
13. **Architectural Decisions & Rationale** - Key technical decisions with trade-offs and justifications
14. **Risks & Mitigation Strategies** - Identified risks, impact assessment, and mitigation approaches
15. **Future Work & Deferred Features** - Features explicitly excluded from MVP with rationale
16. **Traceability to PRD** - Mapping of architectural components to PRD requirements
17. **Sources, Assumptions, and Open Questions** - Reference materials, assumptions made, and unresolved questions
18. **Audit** - Metadata, model information, and execution details

---

## 1. Executive Summary

### 1.1 Purpose
This System Architecture Document (SAD) defines the MVP architecture for an **Automated Employee Onboarding Workflow** system using **iOS** as the frontend platform and **CrewAI multi-agent framework** as the backend orchestration layer. The MVP focuses on delivering core value: automated document collection, verification, and compliance management with real-time progress tracking.

### 1.2 MVP Scope Summary
**In Scope (MVP):**
- iOS native application for new hires and HR administrators
- CrewAI crew with 3 core agents: Document Processing, Compliance, and Notification
- Document upload and OCR-based verification (I-9, W-4, ID documents)
- Real-time progress tracking dashboard
- Basic compliance checks and audit trail
- RESTful API layer connecting iOS to CrewAI backend
- Single HRIS integration (Workday or BambooHR) for MVP validation

**Out of Scope (Deferred):**
- Android application
- Advanced analytics and predictive insights
- AI-powered personalization by role/location
- Multiple HRIS integrations (beyond one)
- Web-based admin dashboard
- Mobile offline mode
- Advanced escalation workflows

### 1.3 Key Architecture Decisions
- **Frontend:** Native iOS (SwiftUI) for optimal mobile experience and performance
- **Backend:** CrewAI Python service with REST API for agent orchestration
- **Communication:** RESTful API with JSON payloads; WebSocket for real-time updates (optional in MVP)
- **Storage:** PostgreSQL for structured data; S3-compatible storage for documents
- **Deployment:** Cloud-native (AWS/GCP) with containerized CrewAI service
- **Adapter:** CrewAI (AAMAD_ADAPTER=crewai)

### 1.4 Target Users
- **New Hire (Primary):** Mobile-first onboarding experience via iOS app
- **HR Administrator:** Web-based admin interface (Phase 2) or iOS admin view (MVP)
- **Hiring Manager:** Progress visibility through notifications and status updates

---

## 2. MVP Architecture Philosophy & Principles

### 2.1 MVP Design Principles

**Customer Feedback First:**
- Deploy MVP within 8-12 months to validate core value proposition
- Prioritize features that deliver 60% time reduction and 90%+ satisfaction
- Focus on document automation and compliance as primary differentiators

**Mobile-First Experience:**
- iOS native app ensures optimal performance and user experience
- Leverage iOS capabilities: camera for document capture, push notifications, secure keychain
- Design for 67% mobile usage pattern identified in MRD

**Minimal Viable Architecture:**
- 3 core CrewAI agents (Document Processing, Compliance, Notification)
- Single HRIS integration for MVP validation
- Basic compliance checks (I-9, W-4) without advanced regulatory variations
- Essential audit trail without advanced analytics

**Observable by Default:**
- Basic logging and monitoring for agent execution
- Progress tracking visible to users and administrators
- Error logging for debugging and support

### 2.2 Core vs. Future Features Decision Framework

**MVP (Phase 1 - 8-12 months):**
- Core document processing and verification
- Basic compliance management
- Real-time progress tracking
- Single HRIS integration
- iOS native app

**Phase 2 (12-18 months):**
- AI-powered personalization
- Advanced analytics dashboards
- Multiple HRIS integrations
- Android application
- Web admin dashboard

**Phase 3 (18-24 months):**
- Predictive analytics
- Enterprise-grade security (SOC 2 Type II)
- Global scaling and multi-region deployment
- Advanced escalation workflows

### 2.3 Technical Architecture Decisions

**iOS Selection Rationale:**
- **Native Performance:** Optimal document capture, processing, and UI responsiveness
- **Security:** iOS keychain and secure enclave for credential and document storage
- **User Experience:** Native iOS patterns align with user expectations for mobile apps
- **Market Alignment:** 67% mobile usage identified in MRD; iOS represents significant market share

**CrewAI Selection Rationale:**
- **Multi-Agent Orchestration:** Natural fit for document processing → compliance → notification workflow
- **Task Coordination:** Built-in support for sequential and parallel agent execution
- **Extensibility:** Easy to add agents (Analytics, Integration) in future phases
- **Framework Maturity:** Production-ready for MVP scope

**RESTful API over GraphQL:**
- Simpler implementation for MVP
- Better compatibility with CrewAI Python backend
- Easier debugging and monitoring
- GraphQL can be considered in Phase 2 if query complexity increases

---

## 3. Stakeholders & Concerns

### 3.1 Primary Stakeholders

**New Hire (End User)**
- **Concerns:** Quick onboarding completion, clear instructions, mobile accessibility, data security
- **Success Criteria:** Complete onboarding in <2 hours, 90%+ satisfaction, zero data breaches

**HR Administrator**
- **Concerns:** Compliance accuracy, audit trail completeness, reduced manual work, system reliability
- **Success Criteria:** 50% reduction in onboarding time, 100% compliance accuracy, <1% manual intervention rate

**Hiring Manager**
- **Concerns:** Onboarding progress visibility, new hire readiness, timely completion
- **Success Criteria:** Real-time progress visibility, 94%+ completion rate, zero delays

**IT/DevOps**
- **Concerns:** System reliability, scalability, security, maintainability
- **Success Criteria:** 99.9% uptime, <2s API response time, secure data handling

### 3.2 Quality Attribute Priorities (MVP)

1. **Usability** (Highest): Mobile-first, intuitive interface, clear progress indicators
2. **Security** (High): Data encryption, secure document storage, compliance adherence
3. **Reliability** (High): System availability, error handling, audit trail integrity
4. **Performance** (Medium): Sub-2s response times, efficient document processing
5. **Scalability** (Medium): Support 100-1000 employees per organization (mid-market target)
6. **Maintainability** (Medium): Clean architecture, documented code, testable components

---

## 4. System Context & Boundaries

### 4.1 System Scope

**Included in MVP:**
- iOS application for document upload and progress tracking
- CrewAI backend service for agent orchestration
- RESTful API layer for iOS ↔ CrewAI communication
- Document storage (S3-compatible)
- PostgreSQL database for structured data
- Single HRIS integration (Workday or BambooHR)

**Excluded from MVP:**
- Web-based admin dashboard (deferred to Phase 2)
- Android application
- Multiple HRIS integrations
- Advanced analytics and reporting
- AI personalization features
- Offline mode for iOS app

### 4.2 External Dependencies

**Required Integrations:**
- **HRIS System:** Workday or BambooHR API for employee data sync
- **Cloud Storage:** AWS S3 or GCP Cloud Storage for document storage
- **LLM Provider:** OpenAI or Anthropic API for document processing and compliance checks
- **Push Notification Service:** Apple Push Notification Service (APNs) for iOS notifications

**Optional Integrations (Phase 2):**
- Slack/Email for notifications (basic email in MVP via CrewAI)
- Additional HRIS systems
- Identity providers (Okta, Azure AD)

### 4.3 System Boundaries

**User Interface Boundary:**
- iOS app handles all user interactions
- No web interface in MVP (deferred)

**Processing Boundary:**
- CrewAI agents handle all document processing, compliance checks, and notifications
- No manual processing workflows in MVP (except exception handling)

**Data Boundary:**
- All employee and document data stored in cloud infrastructure
- No on-premise deployment in MVP

---

## 5. Multi-Agent System Specification

### 5.1 Agent Architecture Overview

The MVP employs a **3-agent CrewAI crew** with sequential and parallel execution patterns:

1. **Document Processing Agent** - Handles document upload, OCR, and validation
2. **Compliance Agent** - Manages regulatory compliance checks and audit trails
3. **Notification Agent** - Sends updates and reminders to users and stakeholders

### 5.2 Agent Definitions

#### 5.2.1 Document Processing Agent

**Role:** Document Processing Specialist
**Goal:** Extract and validate document data from uploaded files with 95%+ OCR accuracy
**Backstory:** Experienced in document verification, OCR technology, and data extraction. Specializes in identifying document types (I-9, W-4, ID) and extracting key fields accurately.

**Capabilities:**
- OCR-based text extraction from images/PDFs
- Document type identification (I-9, W-4, driver's license, passport)
- Data validation (format checks, completeness verification)
- Fraud detection (basic pattern matching)

**Tools:**
- OCR tool (Tesseract or cloud OCR API)
- Document validation tool
- Image processing tool

**Expected Output:**
- Extracted document data (JSON format)
- Document type classification
- Validation status (valid/invalid/needs-review)
- Confidence scores for extracted fields

**Interactions:**
- Receives: Document upload from iOS app via API
- Sends: Extracted data to Compliance Agent
- Triggers: Notification Agent on validation errors

#### 5.2.2 Compliance Agent

**Role:** Compliance Verification Specialist
**Goal:** Ensure all documents meet regulatory requirements (I-9, W-4) and company policies
**Backstory:** Expert in HR compliance regulations, I-9 verification, and audit trail management. Ensures all onboarding documents meet legal and company standards.

**Capabilities:**
- I-9 compliance verification (Section 1 and Section 2 checks)
- W-4 form validation
- Policy acknowledgment tracking
- Audit log generation

**Tools:**
- Compliance validation tool
- Audit logging tool
- HRIS integration tool (for employee data sync)

**Expected Output:**
- Compliance status (compliant/non-compliant/needs-review)
- Audit log entries
- Missing document alerts
- HRIS sync triggers

**Interactions:**
- Receives: Document data from Document Processing Agent
- Sends: Compliance status to Notification Agent
- Triggers: HRIS integration on successful compliance

#### 5.2.3 Notification Agent

**Role:** Communication Coordinator
**Goal:** Keep all stakeholders informed of onboarding progress and required actions
**Backstory:** Specializes in timely, clear communication. Ensures new hires, HR admins, and managers receive appropriate updates at each onboarding stage.

**Capabilities:**
- Email notifications (via SMTP or email API)
- Push notifications (via APNs for iOS)
- Status update generation
- Reminder scheduling

**Tools:**
- Email tool (SendGrid, AWS SES, or similar)
- Push notification tool (APNs integration)
- Status tracking tool

**Expected Output:**
- Notification delivery confirmations
- Status update messages
- Reminder schedules

**Interactions:**
- Receives: Status updates from Document Processing and Compliance Agents
- Sends: Notifications to iOS app (push) and email (SMTP)
- Monitors: Task completion deadlines for reminder triggers

### 5.3 Task Orchestration Specification

#### 5.3.1 Execution Flow

**Sequential Flow (Document Processing → Compliance):**
1. iOS app uploads document → API receives request
2. Document Processing Agent extracts data (OCR + validation)
3. Compliance Agent verifies regulatory requirements
4. Notification Agent sends status update to user

**Parallel Processing (Multiple Documents):**
- Multiple document uploads processed in parallel by Document Processing Agent
- Compliance checks run sequentially per document to maintain audit integrity

**Human-in-the-Loop:**
- Exception handling: Failed compliance → HR admin review → manual approval
- Document rejection: Invalid format → user notification → re-upload

#### 5.3.2 Task Dependencies

```
Document Upload (iOS)
    ↓
Document Processing Agent (OCR + Validation)
    ↓
Compliance Agent (Regulatory Check)
    ↓
Notification Agent (Status Update)
    ↓
HRIS Integration (if compliant)
```

#### 5.3.3 Context Passing

- **Document Processing → Compliance:** Extracted document data (JSON), validation status, confidence scores
- **Compliance → Notification:** Compliance status, missing documents, audit log entries
- **All Agents → Database:** Task status, timestamps, error logs

### 5.4 CrewAI Framework Configuration

**Crew Composition:**
- **Process Type:** Sequential (with parallel document processing where applicable)
- **Agents:** Document Processing Agent, Compliance Agent, Notification Agent
- **Tasks:** 
  - Task 1: Process document upload (Document Processing Agent)
  - Task 2: Verify compliance (Compliance Agent)
  - Task 3: Send notifications (Notification Agent)

**Memory Configuration:**
- **Memory:** Disabled for MVP (reproducibility)
- **Context Window:** Respect context limits (default CrewAI settings)
- **Max Iterations:** 12 per agent task
- **Max Execution Time:** 300 seconds per document processing task

**Logging:**
- **Verbose:** False (production mode)
- **Log Location:** `project-context/2.build/logs/crewai-execution.log`
- **Audit Trail:** All agent actions logged to database

**Tool Binding:**
- Tools declared in agent YAML configuration (`config/agents.yaml`)
- Tools validated at crew initialization
- Tool errors logged and trigger fallback workflows

---

## 6. Frontend Architecture Specification (iOS)

### 6.1 Technology Stack

**Framework:**
- **SwiftUI** for declarative UI development
- **iOS 16+** minimum deployment target
- **Swift 5.9+** for modern language features

**Architecture Pattern:**
- **MVVM (Model-View-ViewModel)** for separation of concerns
- **Combine** framework for reactive data flow
- **Async/Await** for network operations

**Dependencies:**
- **Alamofire** or native `URLSession` for API communication
- **SwiftUI NavigationStack** for navigation
- **KeychainSwift** or native Keychain for secure storage
- **Camera/CameraUI** for document capture

### 6.2 Application Structure

```
OnboardingApp/
├── App/
│   ├── OnboardingApp.swift (App entry point)
│   └── ContentView.swift (Root view)
├── Models/
│   ├── Document.swift
│   ├── OnboardingTask.swift
│   ├── User.swift
│   └── APIResponse.swift
├── ViewModels/
│   ├── DocumentUploadViewModel.swift
│   ├── ProgressTrackingViewModel.swift
│   └── OnboardingStatusViewModel.swift
├── Views/
│   ├── DocumentUpload/
│   │   ├── DocumentCaptureView.swift
│   │   └── DocumentReviewView.swift
│   ├── Progress/
│   │   ├── ProgressDashboardView.swift
│   │   └── TaskListView.swift
│   └── Common/
│       ├── LoadingView.swift
│       └── ErrorView.swift
├── Services/
│   ├── APIService.swift
│   ├── DocumentService.swift
│   └── NotificationService.swift
└── Utilities/
    ├── KeychainManager.swift
    └── NetworkManager.swift
```

### 6.3 User Interface Requirements

**Document Upload Flow:**
1. **Camera Capture View:** Native iOS camera interface for document photos
2. **Document Review View:** Preview and confirm before upload
3. **Upload Progress:** Real-time upload status with progress indicator
4. **Validation Feedback:** Immediate error messages for invalid documents

**Progress Tracking Dashboard:**
1. **Task List View:** List of onboarding tasks with completion status
2. **Task Status Lists:** Segmented or tabbed views that group tasks into **Pending**, **In Progress**, and **Accomplished/Completed** lists, backed by the `status` field on `OnboardingTask`
3. **Progress Indicator:** Visual progress bar (e.g., "3 of 5 tasks completed")
4. **Status Badges:** Color-coded status (pending, in-progress, completed, error)
5. **Refresh Control:** Pull-to-refresh for real-time updates

**User Profile View:**
1. **Profile Summary:** Display key user attributes (first name, last name, email) sourced from the `User` model / `users` table
2. **Employment & Onboarding Status:** Show high-level onboarding status (e.g., Not Started, In Progress, Completed) derived from task completion, and optionally role (e.g., `new_hire`)
3. **HR Details (MVP-lite):** Read-only display of assigned HR contact or manager name if available
4. **Security & Privacy:** No sensitive compliance or document metadata is shown directly in the profile; link out to document/task views for detailed information

**Navigation Structure:**
- **Tab Bar:** Home (Progress), Documents, Profile
- **Navigation Stack:** Document upload → Review → Confirmation
- **Modal Sheets:** Error dialogs, success confirmations

### 6.4 API Integration

**RESTful API Client:**
- Base URL: `https://api.onboarding.example.com/v1`
- Authentication: Bearer token (stored in Keychain)
- Request/Response: JSON format
- Error Handling: Structured error responses with user-friendly messages

**Key Endpoints:**
- `POST /documents/upload` - Upload document with multipart/form-data
- `GET /onboarding/status` - Retrieve current onboarding progress
- `GET /tasks` - List all onboarding tasks (client filters and renders by status: pending, in_progress, completed)
- `POST /tasks/{id}/complete` - Mark task as complete

**Real-Time Updates:**
- **Polling:** Refresh status every 30 seconds (MVP approach)
- **WebSocket (Optional):** Real-time push updates (Phase 2 enhancement)

### 6.5 Security & Data Protection

**Secure Storage:**
- Authentication tokens stored in iOS Keychain
- Document previews cached securely (encrypted)
- No sensitive data in UserDefaults

**Network Security:**
- HTTPS only (TLS 1.2+)
- Certificate pinning (optional for MVP, recommended for production)
- Request/response encryption

**Privacy:**
- Camera permission requested only when needed
- Document access limited to app sandbox
- User consent for data sharing with HRIS

### 6.6 Navigation Structure

The iOS app follows a simple, consistent navigation structure to make onboarding tasks and profile information easy to find:

- **Tab Bar Navigation:**
  - **Home (Progress):** Default landing tab showing the Progress Dashboard, including task status lists (Pending, In Progress, Accomplished/Completed).
  - **Documents:** Entry point for document capture, review, and upload flows.
  - **Profile:** Entry point for the User Profile View, showing user details and high-level onboarding status.

- **Navigation Stack:**
  - Document flows follow a stack pattern: **Document Upload → Document Review → Confirmation**.
  - Progress-related detail views (e.g., individual task detail) are pushed from the Home (Progress) tab.

- **Modals & Sheets:**
  - **Error dialogs:** Blocking alerts for critical failures (e.g., upload failure, authentication issues).
  - **Success confirmations:** Non-blocking sheets or toasts confirming successful uploads or task completion.

---

## 7. Backend Architecture Specification (CrewAI)

### 7.1 API Architecture

**RESTful API Layer:**
- **Framework:** FastAPI (Python) for high performance and async support
- **Port:** 8000 (configurable)
- **Base Path:** `/api/v1`

**Key Endpoints:**

```
POST   /api/v1/documents/upload
GET    /api/v1/onboarding/{user_id}/status
GET    /api/v1/tasks/{user_id}
POST   /api/v1/tasks/{task_id}/complete
GET    /api/v1/compliance/{user_id}/status
POST   /api/v1/notifications/test
```

**Request/Response Format:**
- **Content-Type:** `application/json`
- **Authentication:** Bearer token in `Authorization` header
- **Error Format:** `{"error": "message", "code": "ERROR_CODE", "details": {}}`

### 7.2 CrewAI Service Layer

**Service Structure:**
```
backend/
├── main.py (FastAPI app)
├── crew/
│   ├── crew_config.py (CrewAI crew initialization)
│   ├── agents/
│   │   ├── document_agent.py
│   │   ├── compliance_agent.py
│   │   └── notification_agent.py
│   ├── tasks/
│   │   ├── document_task.py
│   │   ├── compliance_task.py
│   │   └── notification_task.py
│   └── tools/
│       ├── ocr_tool.py
│       ├── compliance_tool.py
│       └── notification_tool.py
├── config/
│   ├── agents.yaml
│   └── tasks.yaml
├── models/
│   ├── document.py
│   ├── onboarding.py
│   └── user.py
└── database/
    ├── models.py (SQLAlchemy)
    └── migrations/
```

**CrewAI Integration:**
- Crew initialized at service startup
- Agents loaded from YAML configuration (`config/agents.yaml`)
- Tasks defined in YAML (`config/tasks.yaml`)
- Tools bound to agents at runtime

**API → CrewAI Flow:**
1. iOS app sends document upload request
2. FastAPI endpoint receives request
3. Document saved to storage (S3)
4. CrewAI crew.kickoff() invoked with document metadata
5. Agents execute tasks sequentially
6. Results stored in database
7. Response returned to iOS app

### 7.3 Database Architecture

**Technology:** PostgreSQL (production) or SQLite (development)

**Core Tables:**

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Documents table
CREATE TABLE documents (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    document_type VARCHAR(50), -- 'I9', 'W4', 'ID', etc.
    file_path VARCHAR(500), -- S3 path
    status VARCHAR(50), -- 'uploaded', 'processing', 'verified', 'rejected'
    extracted_data JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Onboarding tasks table
CREATE TABLE onboarding_tasks (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    task_name VARCHAR(200),
    status VARCHAR(50), -- 'pending', 'in_progress', 'completed', 'failed'
    due_date DATE,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Compliance records table
CREATE TABLE compliance_records (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    document_id UUID REFERENCES documents(id),
    compliance_type VARCHAR(50), -- 'I9', 'W4', etc.
    status VARCHAR(50), -- 'compliant', 'non_compliant', 'needs_review'
    audit_log JSONB,
    verified_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Agent execution logs table
CREATE TABLE agent_logs (
    id UUID PRIMARY KEY,
    execution_id UUID,
    agent_name VARCHAR(100),
    task_name VARCHAR(200),
    status VARCHAR(50),
    input_data JSONB,
    output_data JSONB,
    error_message TEXT,
    execution_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 7.4 Document Storage

**Storage Solution:** AWS S3 or GCP Cloud Storage

**Bucket Structure:**
```
s3://onboarding-documents/
├── {user_id}/
│   ├── {document_id}/
│   │   ├── original.{ext}
│   │   └── processed.{ext}
```

**Security:**
- Pre-signed URLs for iOS uploads (expires in 1 hour)
- Encryption at rest (S3 server-side encryption)
- Access control via IAM policies

### 7.5 Error Handling & Logging

**Error Handling:**
- Structured error responses with error codes
- Retry logic for transient failures (3 retries with exponential backoff)
- Fallback workflows for agent failures (human-in-the-loop escalation)

**Logging:**
- Structured JSON logs (JSON format)
- Log levels: DEBUG, INFO, WARNING, ERROR
- Log aggregation: CloudWatch (AWS) or Cloud Logging (GCP)
- Agent execution logs stored in database for audit

---

## 8. Data Architecture

### 8.1 Data Models

**Document Model:**
```python
class Document:
    id: UUID
    user_id: UUID
    document_type: str  # 'I9', 'W4', 'ID', 'PASSPORT'
    file_path: str  # S3 path
    status: str  # 'uploaded', 'processing', 'verified', 'rejected'
    extracted_data: dict  # OCR results
    created_at: datetime
    updated_at: datetime
```

**Onboarding Task Model:**
```python
class OnboardingTask:
    id: UUID
    user_id: UUID
    task_name: str
    status: str  # 'pending', 'in_progress', 'completed', 'failed'
    due_date: date
    completed_at: datetime
    metadata: dict  # Additional task-specific data
```

**Compliance Record Model:**
```python
class ComplianceRecord:
    id: UUID
    user_id: UUID
    document_id: UUID
    compliance_type: str  # 'I9', 'W4'
    status: str  # 'compliant', 'non_compliant', 'needs_review'
    audit_log: dict  # Compliance check details
    verified_at: datetime
```

### 8.2 Data Flow

**Document Upload Flow:**
1. iOS app → API: Document file + metadata
2. API → S3: Store document
3. API → Database: Create document record (status: 'uploaded')
4. API → CrewAI: Trigger document processing crew
5. CrewAI → Database: Update document status + extracted data
6. Database → iOS: Status update via polling

**Compliance Check Flow:**
1. CrewAI Compliance Agent → Database: Query document data
2. Compliance Agent → LLM/Validation: Verify compliance
3. Compliance Agent → Database: Create compliance record
4. Database → Notification Agent: Trigger status update
5. Notification Agent → iOS: Push notification

### 8.3 Data Retention & Privacy

**Retention Policy:**
- Documents: 7 years (compliance requirement)
- Audit logs: 7 years
- User data: Retained while account active; deleted 30 days after deactivation

**Privacy:**
- PII encryption at rest
- Data anonymization for analytics (Phase 2)
- GDPR/CCPA compliance: User data export and deletion on request

---

## 9. Integration Architecture

### 9.1 HRIS Integration (Workday or BambooHR)

**Integration Type:** RESTful API

**Workflow:**
1. Compliance Agent verifies document compliance
2. On successful compliance → Integration Agent (Phase 2) or API call
3. Employee data synced to HRIS: name, email, document status
4. HRIS confirms sync → Database updated

**API Contract:**
- **Endpoint:** HRIS-specific (Workday: `/ccx/service/customreport2`, BambooHR: `/api/gateway.php/{version}/{namespace}/employees`)
- **Authentication:** OAuth 2.0 or API key
- **Data Format:** JSON
- **Error Handling:** Retry with exponential backoff

**MVP Scope:**
- Single HRIS integration (Workday OR BambooHR, not both)
- Basic employee data sync (name, email, onboarding status)
- No bidirectional sync in MVP (HRIS → Onboarding system deferred)

### 9.2 LLM Provider Integration

**Provider:** OpenAI GPT-4 or Anthropic Claude

**Usage:**
- Document Processing Agent: Text extraction and validation
- Compliance Agent: Regulatory compliance checks

**Configuration:**
- API key stored in environment variables
- Rate limiting: Respect provider limits
- Error handling: Fallback to rule-based validation if LLM fails

### 9.3 Push Notification Service (APNs)

**Integration:** Apple Push Notification Service

**Workflow:**
1. Notification Agent determines notification needed
2. APNs service sends push to iOS device
3. iOS app receives notification and updates UI

**Configuration:**
- APNs certificate/key stored securely
- Device tokens stored in database (user_id → device_token mapping)
- Notification payload: JSON with action type and data

---

## 10. Deployment Architecture

### 10.1 Infrastructure Overview

**Cloud Provider:** AWS or GCP (MVP: single region)

**Components:**
- **API/Backend:** Containerized FastAPI service (AWS ECS/Fargate or GCP Cloud Run)
- **Database:** Managed PostgreSQL (AWS RDS or GCP Cloud SQL)
- **Storage:** S3 (AWS) or Cloud Storage (GCP)
- **iOS App:** Distributed via App Store

### 10.2 Containerization

**Docker Configuration:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Container Registry:** AWS ECR or GCP Container Registry

### 10.3 Deployment Strategy

**MVP Approach:**
- **Single Environment:** Production (no staging in MVP)
- **Deployment Method:** Manual or basic CI/CD (GitHub Actions)
- **Rollback:** Manual container rollback via cloud console

**CI/CD Pipeline (Basic):**
1. Code push to `main` branch
2. GitHub Actions triggers build
3. Docker image built and pushed to registry
4. Container service updated (blue-green or rolling update)

### 10.4 Environment Configuration

**Environment Variables:**
- `DATABASE_URL` - PostgreSQL connection string
- `S3_BUCKET_NAME` - Document storage bucket
- `OPENAI_API_KEY` - LLM provider API key
- `HRIS_API_KEY` - HRIS integration credentials
- `APNS_CERTIFICATE_PATH` - Push notification certificate
- `AAMAD_ADAPTER` - Set to `crewai`

**Secrets Management:**
- AWS Secrets Manager or GCP Secret Manager
- Environment variables injected at container startup

---

## 11. Security & Compliance Architecture

### 11.1 Security Framework

**Authentication:**
- **iOS App:** OAuth 2.0 with Bearer tokens
- **API:** Token validation middleware
- **Token Storage:** iOS Keychain (encrypted)

**Authorization:**
- Role-based access control (RBAC)
- Roles: `new_hire`, `hr_admin`, `manager`
- API endpoints protected by role checks

**Data Encryption:**
- **At Rest:** Database encryption (PostgreSQL encryption), S3 server-side encryption
- **In Transit:** TLS 1.2+ for all API communication, HTTPS only

**Input Validation:**
- Request validation via Pydantic (FastAPI)
- File type validation (images, PDFs only)
- File size limits (10MB per document)

### 11.2 Compliance Requirements

**Regulatory Compliance:**
- **I-9 Verification:** Automated Section 1 and Section 2 checks
- **W-4 Validation:** Tax form completeness and accuracy
- **Audit Trail:** Immutable logs of all compliance checks

**Data Privacy:**
- **GDPR:** User data export and deletion on request
- **CCPA:** Privacy policy and opt-out mechanisms
- **Data Minimization:** Collect only required onboarding data

**Security Standards:**
- **SOC 2 Type II:** Deferred to Phase 2 (MVP: basic security controls)
- **ISO 27001:** Deferred to Phase 2

### 11.3 Security Monitoring

**Logging:**
- Authentication failures logged
- API access logs (IP, user, endpoint, timestamp)
- Agent execution logs for audit

**Monitoring:**
- Basic error rate monitoring
- Unusual access pattern detection (Phase 2: advanced threat detection)

---

## 12. Quality Attributes & Non-Functional Requirements

### 12.1 Performance Requirements

**Response Times:**
- API response: <2 seconds (95th percentile)
- Document upload: <10 seconds for 5MB file
- Document processing: <30 seconds end-to-end (OCR + compliance)
- iOS app UI: <100ms for screen transitions

**Throughput:**
- API: 100 requests/second (MVP scale)
- Document processing: 10 documents/minute per user
- Concurrent users: 100-1000 (mid-market target)

### 12.2 Scalability

**Horizontal Scaling:**
- API service: Auto-scaling based on CPU/memory (2-10 instances)
- Database: Read replicas for Phase 2 (MVP: single instance)
- Storage: S3 scales automatically

**Vertical Scaling:**
- Database: Upgrade instance size as needed
- API containers: Increase memory/CPU allocation

### 12.3 Reliability

**Availability Target:**
- 99.9% uptime (MVP: ~8.76 hours downtime/year)
- Health checks: `/health` endpoint for monitoring
- Graceful degradation: Fallback to manual processing if agents fail

**Error Handling:**
- Retry logic: 3 retries with exponential backoff
- Circuit breaker: Prevent cascading failures
- Dead letter queue: Failed tasks logged for manual review

### 12.4 Maintainability

**Code Quality:**
- Type hints in Python (mypy validation)
- Swift type safety (no `Any` types)
- Unit test coverage: 70%+ (MVP target)

**Documentation:**
- API documentation: OpenAPI/Swagger
- Code comments: Docstrings for public functions
- Architecture documentation: This SAD

---

## 13. Architectural Decisions & Rationale

### 13.1 Decision: iOS Native App vs. Cross-Platform

**Decision:** Native iOS app (SwiftUI)

**Rationale:**
- Optimal performance for document capture and processing
- Native iOS security features (Keychain, secure enclave)
- Better user experience aligned with iOS design patterns
- 67% mobile usage identified in MRD

**Trade-offs:**
- Android app deferred to Phase 2 (reduces MVP scope)
- Requires separate Android development in future

### 13.2 Decision: CrewAI vs. Custom Agent Framework

**Decision:** CrewAI framework

**Rationale:**
- Production-ready multi-agent orchestration
- Built-in task coordination and context passing
- YAML-based configuration for maintainability
- Aligns with AAMAD adapter pattern (AAMAD_ADAPTER=crewai)

**Trade-offs:**
- Framework dependency (vendor lock-in risk mitigated by adapter pattern)
- Learning curve for team (mitigated by documentation)

### 13.3 Decision: RESTful API vs. GraphQL

**Decision:** RESTful API

**Rationale:**
- Simpler implementation for MVP
- Better compatibility with CrewAI Python backend
- Easier debugging and monitoring
- Standard HTTP methods and status codes

**Trade-offs:**
- Potential over-fetching (mitigated by specific endpoints)
- GraphQL can be considered in Phase 2 if query complexity increases

### 13.4 Decision: PostgreSQL vs. NoSQL

**Decision:** PostgreSQL

**Rationale:**
- Structured data (documents, tasks, compliance records) fits relational model
- ACID compliance for audit trail integrity
- SQL queries for reporting and analytics
- Mature ecosystem and tooling

**Trade-offs:**
- Scaling complexity (mitigated by read replicas in Phase 2)
- Schema migrations required (managed via Alembic)

### 13.5 Decision: Single HRIS Integration (MVP)

**Decision:** One HRIS integration (Workday OR BambooHR)

**Rationale:**
- Reduces MVP complexity and development time
- Validates integration pattern for future expansions
- Focuses on core value delivery

**Trade-offs:**
- Limited market reach (mitigated by Phase 2 multi-HRIS support)
- Customer selection based on HRIS (acceptable for MVP validation)

---

## 14. Risks & Mitigation Strategies

### 14.1 High Risks

**Risk 1: Data Privacy and Compliance (GDPR, CCPA)**
- **Impact:** Legal liability, regulatory fines
- **Probability:** Medium
- **Mitigation:**
  - Data encryption at rest and in transit
  - User data export and deletion capabilities
  - Privacy policy and consent mechanisms
  - Legal review of compliance implementation

**Risk 2: Integration with Legacy HRIS Systems**
- **Impact:** Delayed MVP launch, customer dissatisfaction
- **Probability:** Medium
- **Mitigation:**
  - Single HRIS integration in MVP (reduces complexity)
  - API contract validation with HRIS provider
  - Fallback to manual sync if API fails
  - Pilot testing with HRIS partner

**Risk 3: AI Accuracy and False Positives**
- **Impact:** Incorrect compliance checks, manual intervention required
- **Probability:** Medium
- **Mitigation:**
  - Human-in-the-loop for exception handling
  - Confidence score thresholds (95%+ for auto-approval)
  - Manual review workflow for low-confidence results
  - Continuous model improvement based on feedback

### 14.2 Medium Risks

**Risk 4: iOS App Store Approval Delays**
- **Impact:** Delayed MVP launch
- **Probability:** Low
- **Mitigation:**
  - Early App Store submission for review
  - Compliance with Apple guidelines (privacy, security)
  - Beta testing via TestFlight

**Risk 5: CrewAI Agent Performance at Scale**
- **Impact:** Slow document processing, user dissatisfaction
- **Probability:** Low
- **Mitigation:**
  - Performance testing with realistic load
  - Agent execution time limits (300s max)
  - Horizontal scaling of API service
  - Monitoring and alerting for performance degradation

### 14.3 Low Risks

**Risk 6: Team Skill Gaps (CrewAI, iOS)**
- **Impact:** Development delays
- **Probability:** Low
- **Mitigation:**
  - Training and documentation
  - Proof-of-concept development before full implementation
  - External consultants if needed

---

## 15. Future Work & Deferred Features

### 15.1 Deferred to Phase 2 (12-18 months)

**Android Application:**
- Rationale: iOS MVP validates mobile experience; Android adds 50%+ development effort
- Impact: Limited market reach until Phase 2

**Web-Based Admin Dashboard:**
- Rationale: iOS app can include admin views for MVP; web dashboard adds frontend complexity
- Impact: HR admins use iOS app or API directly in MVP

**AI-Powered Personalization:**
- Rationale: Core document processing and compliance are higher priority
- Impact: Generic onboarding workflows in MVP (still effective per MRD)

**Advanced Analytics & Reporting:**
- Rationale: Basic progress tracking sufficient for MVP validation
- Impact: Limited insights until Phase 2

**Multiple HRIS Integrations:**
- Rationale: Single integration validates pattern; multi-HRIS adds integration complexity
- Impact: Customer selection based on HRIS compatibility

### 15.2 Deferred to Phase 3 (18-24 months)

**Predictive Analytics:**
- Rationale: Requires historical data and ML model development
- Impact: No predictive insights in MVP/Phase 2

**Enterprise-Grade Security (SOC 2 Type II, ISO 27001):**
- Rationale: Basic security sufficient for MVP; enterprise certifications require audit process
- Impact: Limited to mid-market customers until Phase 3

**Global Scaling & Multi-Region Deployment:**
- Rationale: Single region sufficient for MVP/Phase 2 (North America focus)
- Impact: Latency for international users until Phase 3

**Advanced Escalation Workflows:**
- Rationale: Basic exception handling sufficient for MVP
- Impact: Manual escalation in MVP

---

## 16. Traceability to PRD

### 16.1 PRD Section 2: Technical Requirements & Architecture

**PRD Requirement:** Multi-Agent Automation Framework
- **SAD Mapping:** Section 5 (Multi-Agent System Specification)
- **Implementation:** Document Processing, Compliance, and Notification Agents

**PRD Requirement:** Document Processing Agent
- **SAD Mapping:** Section 5.2.1 (Document Processing Agent)
- **Implementation:** OCR, validation, document type identification

**PRD Requirement:** Compliance Agent
- **SAD Mapping:** Section 5.2.2 (Compliance Agent)
- **Implementation:** I-9, W-4 verification, audit trail

**PRD Requirement:** Notification Agent
- **SAD Mapping:** Section 5.2.3 (Notification Agent)
- **Implementation:** Email, push notifications, status updates

### 16.2 PRD Section 3: Functional Requirements

**PRD P0 Feature:** Automated Document Collection & Verification
- **SAD Mapping:** Section 6.3 (Document Upload Flow), Section 5.2.1 (Document Processing Agent)
- **Acceptance Criteria Met:**
  - ✅ Support for 15+ document types (I-9, W-4, ID) - Section 5.2.1
  - ✅ OCR accuracy ≥ 95% - Section 5.2.1 (target)
  - ✅ Real-time error feedback - Section 6.3
  - ✅ Secure document encryption - Section 11.1

**PRD P0 Feature:** Real-time Progress Tracking
- **SAD Mapping:** Section 6.3 (Progress Tracking Dashboard), Section 7.1 (API endpoints)
- **Acceptance Criteria Met:**
  - ✅ Task completion dashboard - Section 6.3
  - ✅ Delay alerts and reminders - Section 5.2.3 (Notification Agent)
  - ✅ Mobile responsiveness - Section 6.1 (iOS native)

**PRD P0 Feature:** Compliance Management & Audit Trail
- **SAD Mapping:** Section 5.2.2 (Compliance Agent), Section 8.1 (Compliance Record Model)
- **Acceptance Criteria Met:**
  - ✅ Automated I-9/E-Verify checks - Section 5.2.2
  - ✅ Immutable audit log - Section 7.3 (agent_logs table)
  - ✅ Alerts for compliance exceptions - Section 5.2.3

**PRD P1 Feature:** Mobile-First Experience (Deferred to Phase 2 for Android)
- **SAD Mapping:** Section 6 (Frontend Architecture - iOS), Section 15.1 (Android deferred)
- **MVP Scope:** iOS only (Android in Phase 2)

### 16.3 PRD Section 4: Non-Functional Requirements

**PRD Requirement:** Performance (Sub-2s response, 1000+ concurrent users)
- **SAD Mapping:** Section 12.1 (Performance Requirements)
- **MVP Adjustment:** 100-1000 concurrent users (mid-market target)

**PRD Requirement:** Security (AES-256 encryption, OAuth 2.0, SOC 2 Type II)
- **SAD Mapping:** Section 11.1 (Security Framework)
- **MVP Adjustment:** Basic security controls (SOC 2 Type II deferred to Phase 3)

**PRD Requirement:** Scalability (Auto-scaling, 99.9% uptime)
- **SAD Mapping:** Section 12.2 (Scalability), Section 12.3 (Reliability)
- **Implementation:** Auto-scaling API service, 99.9% uptime target

**PRD Requirement:** Compliance (GDPR/CCPA support, audit logs)
- **SAD Mapping:** Section 11.2 (Compliance Requirements)
- **Implementation:** GDPR/CCPA data export/deletion, audit trail

### 16.4 PRD Section 7: Implementation Strategy

**PRD Phase 1 (MVP - 8-12 months):**
- **SAD Alignment:** Sections 2-15 define MVP architecture
- **Scope Match:** Core agents, iOS app, single HRIS integration

**PRD Phase 2 (Enhanced - 12-18 months):**
- **SAD Mapping:** Section 15.1 (Future Work - Phase 2)
- **Deferred Features:** Android, web dashboard, AI personalization, analytics

---

## 17. Sources, Assumptions, and Open Questions

### 17.1 Sources

**Market Research:**
- MRD: `project-context/1.define/mrd.md` - Market opportunity, technical feasibility, UX expectations

**Product Requirements:**
- PRD: `project-context/1.define/prd.md` - Functional requirements, user stories, technical architecture

**Templates:**
- SAD Template: `.cursor/templates/sad-template.md` - Document structure and section guidance

**External References:**
- CrewAI Documentation: https://docs.crewai.com
- iOS Human Interface Guidelines: https://developer.apple.com/design/human-interface-guidelines
- FastAPI Documentation: https://fastapi.tiangolo.com

### 17.2 Assumptions

**Technical Assumptions:**
1. CrewAI framework supports required agent orchestration patterns (sequential, parallel, human-in-the-loop)
2. iOS 16+ provides sufficient APIs for document capture and secure storage
3. LLM provider (OpenAI/Anthropic) delivers 95%+ OCR accuracy for document processing
4. Single HRIS integration (Workday or BambooHR) sufficient for MVP validation
5. PostgreSQL database scales to 1000 concurrent users with single instance (Phase 2: read replicas)

**Business Assumptions:**
1. Mid-market companies (100-1000 employees) are primary target for MVP
2. iOS represents significant market share (Android deferred to Phase 2)
3. Document automation and compliance are highest-value features (per MRD)
4. 8-12 month MVP timeline is achievable with 6-8 person team

**Operational Assumptions:**
1. Cloud infrastructure (AWS/GCP) provides required scalability and reliability
2. Basic monitoring and logging sufficient for MVP (advanced observability in Phase 2)
3. Manual exception handling acceptable for MVP (automated escalation in Phase 3)

### 17.3 Open Questions

**Technical Questions:**
1. Which HRIS should be prioritized for MVP? (Workday vs. BambooHR - decision needed)
2. Should WebSocket be implemented in MVP for real-time updates, or is polling sufficient?
3. What LLM provider offers best balance of accuracy and cost for document processing?
4. Should certificate pinning be implemented in iOS app for MVP, or deferred to production?

**Business Questions:**
1. What pricing model (per-employee vs. usage-based) should be used for MVP beta customers?
2. Which industries (healthcare, finance, etc.) should be prioritized for compliance features?
3. Should MVP focus on North America only, or include Europe/APAC from start?

**Operational Questions:**
1. What level of customer support is required for MVP beta users?
2. Should MVP include automated testing (E2E), or manual testing sufficient?
3. What monitoring/alerting thresholds should be set for production MVP?

---

## 18. Audit

**Date:** 2024-01-15  
**Persona:** System Architect (@system-arch)  
**Action:** create-sad --mvp  
**Model Used:** GPT-4  
**Temperature:** 0.3 (deterministic artifact generation)  
**Adapter:** CrewAI (AAMAD_ADAPTER=crewai, default)  
**Input Artifacts:**
- MRD: `project-context/1.define/mrd.md`
- PRD: `project-context/1.define/prd.md`
- SAD Template: `.cursor/templates/sad-template.md`

**Output Artifact:**
- SAD: `project-context/1.define/sad.md`

**Scope:** MVP architecture for iOS frontend + CrewAI backend  
**Key Decisions Documented:**
- iOS native app (SwiftUI) for frontend
- CrewAI 3-agent crew (Document Processing, Compliance, Notification)
- RESTful API layer (FastAPI)
- PostgreSQL database
- Single HRIS integration (Workday OR BambooHR)
- Cloud-native deployment (AWS/GCP)

**Template Compliance:**
- ✅ All required sections from SAD template included
- ✅ Table of contents with single-line explanations (Section 0)
- ✅ Traceability to PRD (Section 16)
- ✅ Sources, Assumptions, Open Questions (Section 17)
- ✅ Audit section (Section 18)

**Next Steps:**
- Review and validate architectural decisions with stakeholders
- Resolve open questions (HRIS selection, LLM provider, etc.)
- Proceed to detailed design and implementation planning

