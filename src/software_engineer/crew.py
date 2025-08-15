from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List, Optional
import os
import logging

from dotenv import load_dotenv
load_dotenv()

# Tool imports with fallback handling
try:
    from crewai_tools import SerperDevTool as WebSearchTool
except Exception:
    try:
        from crewai_tools import DuckDuckGoSearchTool as WebSearchTool
    except Exception:
        WebSearchTool = None

try:
    from crewai_tools import PDFSearchTool as PDFTool
except Exception:
    try:
        from crewai_tools import FileReadTool as PDFTool
    except Exception:
        PDFTool = None

try:
    from crewai_tools import FileReadTool, DirectoryReadTool, CodeDocsSearchTool
except Exception:
    FileReadTool = None
    DirectoryReadTool = None
    CodeDocsSearchTool = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _gemini_embedder_config():
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return None
    return {
        "provider": "google",
        "config": {
            "model": "text-embedding-004",
            "api_key": api_key,
        },
    }


@CrewBase
class SoftwareEngineer():
    """Enhanced SoftwareEngineer crew with YAML-based configuration"""

    def __init__(self):
        super().__init__()

    def _get_common_tools(self) -> List:
        """Get common tools available to most agents"""
        tools = []
        
        try:
            if WebSearchTool:
                tools.append(WebSearchTool())
                logger.info("Added WebSearchTool")
        except Exception as e:
            logger.warning(f"Could not initialize WebSearchTool: {e}")
        
        try:
            if FileReadTool:
                tools.append(FileReadTool())
                logger.info("Added FileReadTool")
        except Exception as e:
            logger.warning(f"Could not initialize FileReadTool: {e}")
        
        return tools

    def _get_document_tools(self) -> List:
        """Get specialized tools for document analysis"""
        tools = self._get_common_tools()
        
        # Add PDF tool if available and configured
        try:
            # Skipping PDFSearchTool to avoid OpenAI dependency; rely on FileReadTool/DirectoryReadTool instead
            pass
        except Exception as e:
            logger.warning(f"Could not initialize PDFTool: {e}")
        
        return tools

    # AGENT DEFINITIONS (using YAML config)

    @agent
    def document_analyst(self) -> Agent:
        """Document analysis specialist with PDF and file reading capabilities"""
        tools = self._get_document_tools()
        return Agent(
            config=self.agents_config['document_analyst'],
            verbose=True,
            tools=tools,
            allow_code_execution=True,
            code_execution_mode="safe"
        )

    def engineering_lead(self) -> Agent:
        """Lead architect and project coordinator"""
        return Agent(
            config=self.agents_config['engineering_lead'],
            verbose=True
        )

    @agent
    def backend_engineer(self) -> Agent:
        """Backend services and API implementation specialist"""
        tools = self._get_common_tools()
        return Agent(
            config=self.agents_config['backend_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            tools=tools
        )

    @agent
    def database_engineer(self) -> Agent:
        """Database design and data layer specialist"""
        tools = self._get_common_tools()
        return Agent(
            config=self.agents_config['database_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            tools=tools
        )

    @agent
    def frontend_engineer(self) -> Agent:
        """JavaFX desktop application specialist"""
        tools = self._get_common_tools()
        return Agent(
            config=self.agents_config['frontend_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            tools=tools
        )

    @agent
    def ux_designer(self) -> Agent:
        """User experience and interface design specialist"""
        tools = self._get_common_tools()
        return Agent(
            config=self.agents_config['ux_designer'],
            verbose=True,
            tools=tools
        )

    @agent
    def test_engineer(self) -> Agent:
        """Quality assurance and test automation specialist"""
        tools = self._get_common_tools()
        return Agent(
            config=self.agents_config['test_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            tools=tools
        )

    @agent
    def devops_engineer(self) -> Agent:
        """Deployment and infrastructure automation specialist"""
        tools = self._get_common_tools()
        return Agent(
            config=self.agents_config['devops_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            tools=tools
        )

    @agent
    def quality_assurance_agent(self) -> Agent:
        """Quality gates and validation specialist"""
        tools = self._get_common_tools()
        return Agent(
            config=self.agents_config['quality_assurance_agent'],
            verbose=True,
            tools=tools,
            allow_code_execution=True,
            code_execution_mode="safe"
        )

    # TASK DEFINITIONS (using YAML config)

    @task
    def ingest_requirements(self) -> Task:
        """Phase 1: Requirements analysis and document ingestion"""
        return Task(
            config=self.tasks_config['ingest_requirements'],
            agent=self.document_analyst(),
            output_file='output/REQUIREMENTS.md'
        )

    @task
    def design_system_architecture(self) -> Task:
        """Phase 2: System architecture design"""
        return Task(
            config=self.tasks_config['design_system_architecture'],
            agent=self.backend_engineer(),
            context=[self.ingest_requirements()],
            output_file='output/ARCHITECTURE.md'
        )

    @task
    def validate_architecture(self) -> Task:
        """Quality Gate: Architecture validation"""
        return Task(
            config=self.tasks_config['validate_architecture'],
            agent=self.quality_assurance_agent(),
            context=[self.ingest_requirements(), self.design_system_architecture()],
            output_file='output/ARCHITECTURE_REVIEW.md'
        )

    @task
    def design_database_layer(self) -> Task:
        """Phase 3a: Database design and data layer"""
        return Task(
            config=self.tasks_config['design_database_layer'],
            agent=self.database_engineer(),
            context=[self.design_system_architecture(), self.validate_architecture()],
            output_file='output/DATABASE_DESIGN.md'
        )

    @task
    def design_user_experience(self) -> Task:
        """Phase 3b: User experience and interface design"""
        return Task(
            config=self.tasks_config['design_user_experience'],
            agent=self.ux_designer(),
            context=[self.design_system_architecture(), self.validate_architecture()],
            output_file='output/UX_DESIGN.md'
        )

    @task
    def implement_backend_services(self) -> Task:
        """Phase 4a: Backend services implementation"""
        return Task(
            config=self.tasks_config['implement_backend_services'],
            agent=self.backend_engineer(),
            context=[
                self.design_system_architecture(),
                self.design_database_layer(),
                self.validate_architecture()
            ]
        )

    @task
    def implement_frontend_application(self) -> Task:
        """Phase 4b: Frontend application implementation"""
        return Task(
            config=self.tasks_config['implement_frontend_application'],
            agent=self.frontend_engineer(),
            context=[
                self.design_system_architecture(),
                self.design_user_experience(),
                self.validate_architecture()
            ]
        )

    @task
    def implement_testing_strategy(self) -> Task:
        """Phase 5: Comprehensive testing implementation"""
        return Task(
            config=self.tasks_config['implement_testing_strategy'],
            agent=self.test_engineer(),
            context=[
                self.implement_backend_services(),
                self.implement_frontend_application()
            ],
            output_file='output/TESTING_STRATEGY.md'
        )

    @task
    def validate_implementation(self) -> Task:
        """Quality Gate: Implementation validation"""
        return Task(
            config=self.tasks_config['validate_implementation'],
            agent=self.quality_assurance_agent(),
            context=[
                self.implement_backend_services(),
                self.implement_frontend_application(),
                self.implement_testing_strategy()
            ],
            output_file='output/IMPLEMENTATION_REVIEW.md'
        )

    @task
    def create_deployment_package(self) -> Task:
        """Phase 6: Deployment automation and packaging"""
        return Task(
            config=self.tasks_config['create_deployment_package'],
            agent=self.devops_engineer(),
            context=[
                self.implement_backend_services(),
                self.implement_frontend_application(),
                self.validate_implementation()
            ],
            output_file='output/DEPLOYMENT_GUIDE.md'
        )

    @task
    def final_project_evaluation(self) -> Task:
        """Final: Project completion and evaluation"""
        return Task(
            config=self.tasks_config['final_project_evaluation'],
            agent=self.quality_assurance_agent(),
            context=[
                self.create_deployment_package(),
                self.validate_implementation()
            ],
            output_file='output/PROJECT_COMPLETION_REPORT.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SoftwareEngineer crew with hierarchical process"""
        
        # Define all tasks in execution order
        tasks = [
            self.ingest_requirements(),
            self.design_system_architecture(),
            self.validate_architecture(),
            self.design_database_layer(),
            self.design_user_experience(),
            self.implement_backend_services(),
            self.implement_frontend_application(),
            self.implement_testing_strategy(),
            self.validate_implementation(),
            self.create_deployment_package(),
            self.final_project_evaluation()
        ]

        embedder_cfg = _gemini_embedder_config()
        return Crew(
            agents=self.agents,
            tasks=tasks,
            process=Process.hierarchical,
            manager_agent=self.engineering_lead(),
            verbose=True,
            memory=bool(embedder_cfg),
            embedder=embedder_cfg if embedder_cfg else None,
        )