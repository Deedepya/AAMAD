# CrewAI Integration Module

Clean, modular CrewAI integration for document upload processing.

## Architecture

### Single Responsibility Principle

Each module has a single, well-defined responsibility:

- **`crew_config.py`** - Loads YAML configurations and creates CrewAI crew
- **`crew_service.py`** - Clean interface between API layer and CrewAI
- **`tools/`** - Individual tool implementations (one file per tool)
- **`tools/tool_registry.py`** - Central registry for all tools

## Structure

```
crew/
├── __init__.py              # Module exports
├── crew_config.py          # YAML loader and crew creator
├── crew_service.py          # Service interface
├── tools/
│   ├── __init__.py         # Tool exports
│   ├── tool_registry.py    # Tool registry
│   ├── ocr_tool.py         # OCR text extraction
│   ├── document_validation_tool.py  # Document validation
│   ├── image_processing_tool.py     # Image optimization
│   ├── compliance_validation_tool.py # Compliance checks
│   ├── audit_logging_tool.py        # Audit trail
│   └── hris_integration_tool.py     # HRIS sync (stub)
└── README.md               # This file
```

## Integration Flow

```
API Layer (document_routes.py)
    ↓
DocumentUploadService
    ↓
DirectDocumentUploadClient
    ↓
CrewAIService (crew_service.py)
    ↓
CrewAI Crew (crew_config.py)
    ↓
Agents → Tools
```

## Configuration

Agents and tasks are configured in YAML files:
- `config/agents.yaml` - Agent definitions
- `config/tasks.yaml` - Task definitions

## Tools Implemented

1. **ocr_tool** - Extracts text from document images
2. **document_validation_tool** - Validates file format, size, content
3. **image_processing_tool** - Optimizes images for OCR
4. **compliance_validation_tool** - Validates regulatory compliance
5. **audit_logging_tool** - Creates audit trail entries
6. **hris_integration_tool** - HRIS sync (stub for MVP)

## Usage

The CrewAI service is automatically initialized in `app_setup/create_app.py` and integrated into the document upload flow. When a document is uploaded:

1. Document is validated by `DocumentUploadService`
2. If valid, `DirectDocumentUploadClient` processes it
3. If CrewAI service is available, document is processed by agents
4. Results are returned to the API layer

## Error Handling

- If CrewAI initialization fails, upload continues without processing
- If CrewAI processing fails, upload succeeds but processing is skipped
- All errors are logged for debugging

## Testing

To test the integration:

```bash
curl -X POST http://localhost:8000/documents/upload \
  -F "file=@/path/to/document.jpg" \
  -F "document_type=I9" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000"
```

The response will include processing status if CrewAI is enabled.

