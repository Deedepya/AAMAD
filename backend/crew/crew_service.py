"""
CrewAI Service Interface
Clean interface between API layer and CrewAI agents
"""

import io
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass

from .crew_config import CrewAIConfig

logger = logging.getLogger(__name__)


@dataclass
class DocumentProcessingResult:
    """Result from document processing crew execution"""
    document_id: str
    document_type: str
    extracted_data: Dict[str, Any]
    validation_status: str
    compliance_status: Optional[str] = None
    compliance_data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class CrewAIService:
    """
    Service interface for CrewAI document processing
    
    Provides clean abstraction between API layer and CrewAI implementation
    """
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize CrewAI service
        
        Args:
            config_dir: Directory containing agents.yaml and tasks.yaml
        """
        self.config = CrewAIConfig(config_dir=config_dir)
        self.crew = None
        self._initialize_crew()
    
    def _initialize_crew(self):
        """Initialize CrewAI crew from configuration"""
        try:
            self.crew = self.config.create_crew()
            logger.info("CrewAI crew initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize CrewAI crew: {str(e)}")
            raise
    
    async def process_document(
        self,
        file: io.BytesIO,
        document_type: str,
        user_id: str,
        document_id: str
    ) -> DocumentProcessingResult:
        """
        Process uploaded document using CrewAI agents
        
        Args:
            file: Document file as BytesIO
            document_type: Type of document (I9, W4, etc.)
            user_id: User identifier
            document_id: Document identifier
            
        Returns:
            DocumentProcessingResult with processing results
        """
        if not self.crew:
            raise RuntimeError("CrewAI crew not initialized")
        
        try:
            # Prepare context for crew execution
            # Store file temporarily for tools to access
            import tempfile
            import os
            
            file_extension = os.path.splitext(file.name if hasattr(file, 'name') else 'document')[1] or '.jpg'
            file_path = os.path.join(tempfile.gettempdir(), f"{document_id}{file_extension}")
            
            with open(file_path, 'wb') as f:
                file.seek(0)
                f.write(file.read())
            
            # Prepare task context as input string
            context_str = f"""
            Document Processing Context:
            - File Path: {file_path}
            - Document ID: {document_id}
            - Document Type: {document_type}
            - User ID: {user_id}
            - Filename: {file.name if hasattr(file, 'name') else 'document'}
            """
            
            # Update first task (process_document_upload) with context
            if self.crew.tasks:
                original_desc = self.crew.tasks[0].description or ""
                self.crew.tasks[0].description = f"{original_desc}\n\n{context_str}"
            
            # Execute crew
            logger.info(f"Executing CrewAI crew for document {document_id}")
            result = self.crew.kickoff()
            
            # Parse results
            processing_result = self._parse_crew_result(
                result=result,
                document_id=document_id,
                document_type=document_type
            )
            
            # Clean up temporary file
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                logger.warning(f"Failed to clean up temp file {file_path}: {str(e)}")
            
            logger.info(f"Document processing completed for {document_id}")
            return processing_result
            
        except Exception as e:
            logger.error(f"Error processing document {document_id}: {str(e)}")
            # Clean up temp file if it exists
            try:
                import os
                import tempfile
                file_extension = os.path.splitext(file.name if hasattr(file, 'name') else 'document')[1] or '.jpg'
                file_path = os.path.join(tempfile.gettempdir(), f"{document_id}{file_extension}")
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception:
                pass
            
            return DocumentProcessingResult(
                document_id=document_id,
                document_type=document_type,
                extracted_data={},
                validation_status="error",
                error=str(e)
            )
    
    def _parse_crew_result(
        self,
        result: Any,
        document_id: str,
        document_type: str
    ) -> DocumentProcessingResult:
        """
        Parse CrewAI execution result into structured format
        
        Args:
            result: Raw result from crew.kickoff()
            document_id: Document identifier
            document_type: Document type
            
        Returns:
            DocumentProcessingResult
        """
        # CrewAI returns results in different formats
        # Try to extract structured data
        extracted_data = {}
        validation_status = "unknown"
        compliance_status = None
        compliance_data = None
        
        try:
            # If result is a string, try to parse as JSON
            if isinstance(result, str):
                import json
                try:
                    result_dict = json.loads(result)
                    extracted_data = result_dict.get("extracted_data", {})
                    validation_status = result_dict.get("validation_status", "unknown")
                    compliance_status = result_dict.get("compliance_status")
                    compliance_data = result_dict.get("compliance_data")
                except json.JSONDecodeError:
                    # If not JSON, treat as text result
                    extracted_data = {"raw_text": result}
                    validation_status = "processed"
            
            # If result has tasks attribute (CrewAI output format)
            elif hasattr(result, 'tasks_output'):
                # Extract from task outputs
                for task_output in result.tasks_output:
                    if isinstance(task_output, dict):
                        extracted_data.update(task_output)
                    elif isinstance(task_output, str):
                        extracted_data["task_output"] = task_output
            
            # If result is a dict
            elif isinstance(result, dict):
                extracted_data = result.get("extracted_data", result)
                validation_status = result.get("validation_status", "processed")
                compliance_status = result.get("compliance_status")
                compliance_data = result.get("compliance_data")
            
        except Exception as e:
            logger.warning(f"Error parsing crew result: {str(e)}, using default values")
            extracted_data = {"raw_result": str(result)}
            validation_status = "processed"
        
        return DocumentProcessingResult(
            document_id=document_id,
            document_type=document_type,
            extracted_data=extracted_data,
            validation_status=validation_status,
            compliance_status=compliance_status,
            compliance_data=compliance_data
        )

