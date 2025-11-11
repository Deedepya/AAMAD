# Project Setup Documentation

## Overview
This document describes the project setup for the **Automated Employee Onboarding Workflow** system, including folder structure, dependencies, environment configuration, and setup instructions.

**Reference Documents:**
- PRD: `project-context/1.define/prd.md`
- SAD: `project-context/1.define/sad.md`

---

## 1. Project Structure

### 1.1 Root Directory Structure
```
AAMAD/
├── .cursor/                    # AAMAD framework files (agents, rules, templates)
├── project-context/
│   ├── 1.define/               # Requirements documents (PRD, SAD, MRD)
│   ├── 2.build/                # Build artifacts (this file, logs, etc.)
│   └── 3.deliver/              # Delivery artifacts (QA, deployment)
├── backend/                    # CrewAI Python backend service
│   ├── crew/                   # CrewAI agent, task, and tool implementations
│   ├── config/                 # YAML configuration files (agents.yaml, tasks.yaml)
│   ├── models/                 # Data models
│   ├── database/               # Database models and migrations
│   └── requirements.txt        # Python dependencies
├── ios/                        # iOS native application
│   └── OnboardingApp/          # SwiftUI app structure
├── .env.example                # Environment variable template
├── .gitignore                  # Git ignore rules
└── README.md                   # Project overview
```

### 1.2 Backend Structure
```
backend/
├── main.py                     # FastAPI application entry point (to be created)
├── crew/
│   ├── crew_config.py          # CrewAI crew initialization (to be created)
│   ├── agents/                 # Agent implementations (to be created)
│   │   └── __init__.py
│   ├── tasks/                  # Task definitions (to be created)
│   │   └── __init__.py
│   └── tools/                  # Tool implementations (to be created)
│       └── __init__.py
├── config/
│   ├── agents.yaml             # ✅ Agent configurations (created)
│   └── tasks.yaml              # ✅ Task configurations (created)
├── models/                     # Data models (to be created)
│   └── __init__.py
├── database/
│   ├── models.py               # ✅ SQLAlchemy model placeholders (created)
│   ├── migrations/             # Alembic migrations (to be created)
│   └── __init__.py
├── requirements.txt            # ✅ Python dependencies (created)
├── .gitignore                  # ✅ Git ignore rules (created)
└── README.md                   # ✅ Backend documentation (created)
```

### 1.3 iOS Structure
```
ios/
├── OnboardingApp/
│   ├── App/                    # App entry point (to be created by @frontend.eng)
│   ├── Models/                 # Data models (to be created)
│   ├── ViewModels/             # MVVM view models (to be created)
│   ├── Views/                  # SwiftUI views (to be created)
│   │   ├── DocumentUpload/
│   │   ├── Progress/
│   │   └── Common/
│   ├── Services/               # API and business logic (to be created)
│   └── Utilities/              # Helper utilities (to be created)
├── .gitignore                  # ✅ Git ignore rules (created)
└── README.md                   # ✅ iOS documentation (created)
```

---

## 2. Dependencies

### 2.1 Backend Dependencies (Python 3.11+)

**Core Framework:**
- `fastapi==0.104.1` - Web framework
- `uvicorn[standard]==0.24.0` - ASGI server
- `pydantic==2.5.0` - Data validation
- `crewai==0.28.8` - Multi-agent framework
- `langchain==0.1.0` - LLM integration

**Database:**
- `sqlalchemy==2.0.23` - ORM
- `alembic==1.12.1` - Database migrations
- `psycopg2-binary==2.9.9` - PostgreSQL driver

**Cloud Storage:**
- `boto3==1.29.7` - AWS S3
- `google-cloud-storage==2.14.0` - GCP Cloud Storage (alternative)

**Document Processing:**
- `pytesseract==0.3.10` - OCR
- `Pillow==10.1.0` - Image processing
- `PyPDF2==3.0.1` - PDF processing

**Notifications:**
- `sendgrid==6.11.0` - Email
- `apns2==0.7.2` - Apple Push Notifications

**Installation:**
```bash
cd backend
pip install -r requirements.txt
```

### 2.2 iOS Dependencies

**Framework:**
- SwiftUI (iOS 16+)
- Swift 5.9+
- Combine framework (reactive programming)

**Dependencies (to be added by @frontend.eng):**
- Alamofire or native URLSession (API communication)
- KeychainSwift or native Keychain (secure storage)
- Camera/CameraUI (document capture)

**Note:** Specific Swift Package Manager or CocoaPods dependencies will be defined during frontend development.

---

## 3. Environment Configuration

### 3.1 Environment Variables

**Important:** The `.env.example` file was not created due to system restrictions. Create a `.env` file manually with the following variables:

**AAMAD Adapter:**
```
AAMAD_ADAPTER=crewai
```

**Database:**
```
DATABASE_URL=postgresql://user:password@localhost:5432/onboarding_db
# For development: DATABASE_URL=sqlite:///./onboarding.db
```

**Cloud Storage (AWS S3):**
```
S3_BUCKET_NAME=onboarding-documents
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
```

**LLM Provider (OpenAI):**
```
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4
```

**HRIS Integration (Workday or BambooHR):**
```
WORKDAY_API_URL=https://your-instance.workday.com/ccx/service/customreport2
WORKDAY_API_KEY=your_workday_api_key
WORKDAY_TENANT=your_tenant
```

**Push Notifications (APNs):**
```
APNS_CERTIFICATE_PATH=path/to/apns_certificate.pem
APNS_KEY_PATH=path/to/apns_key.pem
APNS_TEAM_ID=your_apple_team_id
APNS_KEY_ID=your_apns_key_id
APNS_TOPIC=com.yourcompany.onboardingapp
APNS_USE_SANDBOX=true
```

**Email:**
```
SENDGRID_API_KEY=your_sendgrid_api_key
EMAIL_FROM_ADDRESS=noreply@yourcompany.com
EMAIL_FROM_NAME=Onboarding System
```

**API Configuration:**
```
API_HOST=0.0.0.0
API_PORT=8000
API_BASE_PATH=/api/v1
```

**Security:**
```
SECRET_KEY=your_secret_key_here_change_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**CrewAI Configuration:**
```
CREWAI_VERBOSE=false
CREWAI_MAX_ITER=12
CREWAI_MAX_EXECUTION_TIME=300
CREWAI_MEMORY_ENABLED=false
MAX_RPM=60
```

**Logging:**
```
LOG_LEVEL=INFO
LOG_FILE_PATH=project-context/2.build/logs/crewai-execution.log
```

### 3.2 Setup Instructions

1. **Create `.env` file:**
   ```bash
   # Copy the environment variables listed above into a .env file
   # Replace placeholder values with actual credentials
   ```

2. **Load environment variables:**
   - Backend: Uses `python-dotenv` to load `.env` automatically
   - iOS: Environment variables configured in Xcode scheme (to be done by @frontend.eng)

---

## 4. CrewAI Configuration

### 4.1 Agent Configuration (`backend/config/agents.yaml`)

Three agents are configured:
1. **Document Processing Agent** - OCR and document validation
2. **Compliance Agent** - Regulatory compliance verification
3. **Notification Agent** - Communication and status updates

**Key Settings:**
- `allow_delegation: false` - No delegation for MVP
- `memory: false` - Reproducibility (per AAMAD rules)
- `max_iter: 12` - Maximum iterations per task
- `max_execution_time: 300` - 5-minute timeout per task

### 4.2 Task Configuration (`backend/config/tasks.yaml`)

Three tasks defined:
1. **process_document_upload** - Document OCR and extraction
2. **verify_compliance** - Compliance verification
3. **send_status_notification** - Status notifications

**Execution Flow:**
```
Document Upload → Document Processing → Compliance → Notification
```

---

## 5. Database Setup

### 5.1 Database Schema

**Core Tables (per SAD Section 7.3):**
- `users` - User accounts
- `documents` - Document metadata and extracted data
- `onboarding_tasks` - Task tracking
- `compliance_records` - Compliance verification results
- `agent_logs` - Agent execution audit trail

### 5.2 Migration Setup (to be done by @backend.eng)

```bash
# Initialize Alembic
cd backend
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

---

## 6. Installation Steps

### 6.1 Prerequisites

**System Requirements:**
- Python 3.11+ (backend)
- PostgreSQL 14+ (production) or SQLite (development)
- Xcode 15+ (iOS development)
- macOS (for iOS development)

**External Services:**
- LLM provider account (OpenAI or Anthropic)
- Cloud storage (AWS S3 or GCP Cloud Storage)
- HRIS API access (Workday or BambooHR)
- SendGrid account (email notifications)
- Apple Developer account (APNs)

### 6.2 Backend Setup

```bash
# 1. Navigate to backend directory
cd backend

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file with required variables (see Section 3.1)

# 5. Initialize database (after @backend.eng implements models)
# alembic init alembic
# alembic revision --autogenerate -m "Initial migration"
# alembic upgrade head

# 6. Run development server (after @backend.eng implements main.py)
# uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 6.3 iOS Setup

```bash
# 1. Open Xcode project (to be created by @frontend.eng)
# open ios/OnboardingApp.xcodeproj

# 2. Install dependencies (Swift Package Manager or CocoaPods)
# (Instructions to be provided by @frontend.eng)

# 3. Configure API endpoint in APIService.swift
# (To be implemented by @frontend.eng)

# 4. Build and run
# Cmd+R in Xcode
```

---

## 7. What's Next for Downstream Agents

### 7.1 Frontend Engineer (@frontend.eng)

**Tasks:**
1. Create Xcode project structure in `ios/OnboardingApp/`
2. Implement SwiftUI views per SAD Section 6.3:
   - Document capture view
   - Document review view
   - Progress tracking dashboard
   - Task list view
3. Implement ViewModels (MVVM pattern)
4. Implement API service layer
5. Configure push notifications (APNs)
6. Document implementation in `project-context/2.build/frontend.md`

**Reference:**
- SAD Section 6: Frontend Architecture Specification (iOS)
- SAD Section 6.2: Application Structure

### 7.2 Backend Engineer (@backend.eng)

**Tasks:**
1. Implement FastAPI application (`backend/main.py`)
2. Implement CrewAI crew initialization (`backend/crew/crew_config.py`)
3. Implement agent classes (load from `config/agents.yaml`)
4. Implement task classes (load from `config/tasks.yaml`)
5. Implement tools:
   - OCR tool
   - Compliance validation tool
   - Notification tools (email, push)
   - HRIS integration tool
6. Implement database models (complete `backend/database/models.py`)
7. Create database migrations (Alembic)
8. Implement API endpoints per SAD Section 7.1
9. Document implementation in `project-context/2.build/backend.md`

**Reference:**
- SAD Section 7: Backend Architecture Specification
- SAD Section 5: Multi-Agent System Specification
- SAD Section 7.3: Database Architecture

### 7.3 Integration Engineer (@integration.eng)

**Tasks:**
1. Wire iOS app to backend API endpoints
2. Test end-to-end document upload flow
3. Test progress tracking synchronization
4. Verify push notification delivery
5. Test error handling and retry logic
6. Document integration patterns in `project-context/2.build/integration.md`

**Reference:**
- SAD Section 9: Integration Architecture
- Frontend and Backend implementation artifacts

### 7.4 QA Engineer (@qa.eng)

**Tasks:**
1. Create test plan for MVP features
2. Perform smoke tests on document upload
3. Test compliance verification workflows
4. Verify notification delivery
5. Test error scenarios and edge cases
6. Document test results and known issues in `project-context/2.build/qa.md`

**Reference:**
- SAD Section 12: Quality Attributes & Non-Functional Requirements
- All implementation artifacts

---

## 8. Project Status

### 8.1 Completed ✅

- [x] Root folder structure created
- [x] Backend folder structure created
- [x] iOS folder structure created
- [x] Python dependencies defined (`backend/requirements.txt`)
- [x] CrewAI agent configuration (`backend/config/agents.yaml`)
- [x] CrewAI task configuration (`backend/config/tasks.yaml`)
- [x] Database model placeholders (`backend/database/models.py`)
- [x] Git ignore files (root, backend, iOS)
- [x] README files (backend, iOS)
- [x] Setup documentation (this file)

### 8.2 Pending (Downstream Agents)

- [ ] Backend implementation (FastAPI, CrewAI crew, agents, tasks, tools)
- [ ] iOS app implementation (SwiftUI views, ViewModels, services)
- [ ] Database migrations (Alembic)
- [ ] API integration and testing
- [ ] QA testing and validation

---

## 9. Key Decisions and Rationale

### 9.1 Folder Structure

**Decision:** Separate `backend/` and `ios/` directories at root level.

**Rationale:**
- Clear separation of concerns
- Independent development workflows
- Easier deployment and CI/CD setup
- Aligns with SAD architecture

### 9.2 Configuration Files

**Decision:** YAML-based configuration for CrewAI agents and tasks.

**Rationale:**
- Per AAMAD rules: externalize agent/task definitions to YAML
- Easier maintenance and updates
- No inline Python agent/task definitions
- Supports AAMAD adapter pattern

### 9.3 Environment Variables

**Decision:** Comprehensive `.env` file with all external service credentials.

**Rationale:**
- Security: No hardcoded secrets
- Flexibility: Easy environment switching (dev/staging/prod)
- Per AAMAD rules: All secrets from environment variables

---

## 10. Troubleshooting

### 10.1 Common Issues

**Issue:** `.env.example` file not created
- **Solution:** Create `.env` manually using the template in Section 3.1

**Issue:** Python dependencies fail to install
- **Solution:** Ensure Python 3.11+ is installed. Use virtual environment.

**Issue:** Database connection fails
- **Solution:** Verify `DATABASE_URL` in `.env` matches your database configuration.

**Issue:** CrewAI agent configuration errors
- **Solution:** Validate YAML syntax in `backend/config/agents.yaml` and `tasks.yaml`.

---

## 11. Sources, Assumptions, and Open Questions

### 11.1 Sources

- **PRD:** `project-context/1.define/prd.md` - Product requirements and feature specifications
- **SAD:** `project-context/1.define/sad.md` - System architecture and technical specifications
- **AAMAD Rules:** `.cursor/rules/` - Framework rules and guidelines
- **CrewAI Documentation:** https://docs.crewai.com

### 11.2 Assumptions

1. **Development Environment:**
   - Python 3.11+ available on development machines
   - PostgreSQL or SQLite available for local development
   - Xcode 15+ available for iOS development (macOS required)

2. **External Services:**
   - LLM provider API keys available (OpenAI or Anthropic)
   - Cloud storage credentials available (AWS S3 or GCP)
   - HRIS API access available (Workday or BambooHR)
   - SendGrid account for email notifications
   - Apple Developer account for APNs

3. **Team Capabilities:**
   - Backend engineer familiar with Python, FastAPI, CrewAI
   - Frontend engineer familiar with SwiftUI and iOS development
   - Integration engineer can wire frontend to backend APIs

### 11.3 Open Questions

1. **HRIS Selection:** Which HRIS should be prioritized for MVP? (Workday vs. BambooHR)
2. **LLM Provider:** Which provider offers best balance of accuracy and cost? (OpenAI vs. Anthropic)
3. **Cloud Provider:** AWS vs. GCP for cloud storage and deployment?
4. **Development Database:** Use SQLite for local development or require PostgreSQL from start?

---

## 12. Audit

**Date:** 2024-01-15  
**Persona:** Project Manager (@project.mgr)  
**Action:** setup-project  
**Model Used:** GPT-4  
**Temperature:** 0.3 (deterministic setup)  
**Adapter:** CrewAI (AAMAD_ADAPTER=crewai, default)

**Input Artifacts:**
- PRD: `project-context/1.define/prd.md`
- SAD: `project-context/1.define/sad.md`
- Project Manager Persona: `.cursor/agents/project-mgr.md`

**Output Artifacts:**
- Project structure (folders and files)
- `backend/requirements.txt` - Python dependencies
- `backend/config/agents.yaml` - CrewAI agent configuration
- `backend/config/tasks.yaml` - CrewAI task configuration
- `backend/database/models.py` - Database model placeholders
- `backend/README.md` - Backend documentation
- `ios/README.md` - iOS documentation
- `.gitignore` files (root, backend, iOS)
- `project-context/2.build/setup.md` - This document

**Scope:**
- ✅ Root folder structure created
- ✅ Backend skeleton created (no application code)
- ✅ iOS skeleton created (no application code)
- ✅ Configuration files created (YAML, requirements)
- ✅ Environment variable template documented
- ✅ Setup documentation completed

**Prohibited Actions (Not Performed):**
- ❌ No application logic code created
- ❌ No backend API implementation
- ❌ No iOS app implementation
- ❌ No database migrations created
- ❌ No agent/task/tool implementations

**Next Steps:**
1. Frontend Engineer (@frontend.eng) should run `*develop-fe` to implement iOS app
2. Backend Engineer (@backend.eng) should run `*develop-be` to implement CrewAI backend
3. Integration Engineer (@integration.eng) should run `*integrate-api` to wire frontend and backend
4. QA Engineer (@qa.eng) should run `*qa` to test end-to-end functionality

---

**Setup Complete.** Ready for downstream agent execution.

