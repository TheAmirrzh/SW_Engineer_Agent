from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import os
try:
    from crewai_tools import SerperDevTool as WebSearchTool
except Exception:  # noqa: BLE001 - optional dependency fallback
    from crewai_tools import DuckDuckGoSearchTool as WebSearchTool
try:
    from crewai_tools import PDFSearchTool as PDFTool
except Exception:  # noqa: BLE001 - optional dependency fallback
    try:
        from crewai_tools import FileReadTool as PDFTool
    except Exception:
        PDFTool = None  # type: ignore[assignment]



@CrewBase
class SoftwareEngineer():
    """SoftwareEngineer crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    
    def engineering_lead(self) -> Agent:
        return Agent(
            config=self.agents_config['engineering_lead'],  # type: ignore[index]
            verbose=True
        )

    @agent
    def backend_engineer(self) -> Agent:
        search_tool = WebSearchTool()
        pdf_tool = None
        if PDFTool is not None:
            try:
                project_pdf = os.environ.get('PROJECT_PDF')
                if hasattr(PDFTool, '__name__') and 'PDFSearchTool' in PDFTool.__name__ and project_pdf:
                    pdf_tool = PDFTool(pdf=project_pdf)  # type: ignore[call-arg]
                else:
                    pdf_tool = PDFTool()  # type: ignore[call-arg]
            except Exception:
                pdf_tool = None
        return Agent(
            config=self.agents_config['backend_engineer'],  # type: ignore[index]
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",  # Uses Docker for safety in test tools
            tools=[t for t in [search_tool, pdf_tool] if t is not None]
        )

    @agent
    def database_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['database_engineer'],  # type: ignore[index]
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",  # Uses Docker for safety in test tools
        )

    @agent
    def frontend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_engineer'],  # type: ignore[index]
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",  # Uses Docker for safety in test tools
        )

    @agent
    def ux_designer(self) -> Agent:
        return Agent(
            config=self.agents_config['ux_designer'],  # type: ignore[index]
            verbose=True
        )

    @agent
    def devops_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['devops_engineer'],  # type: ignore[index]
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",  # Uses Docker for safety in test tools
        )

    @agent
    def evaluation_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['evaluation_analyst'],  # type: ignore[index]
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",  # Uses Docker for safety in test tools
        )

    @agent
    def test_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['test_engineer'],  # type: ignore[index]
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",  # Uses Docker for safety in test tools
        )


    @task
    def design_architecture(self) -> Task:
        return Task(
            config=self.tasks_config['design_architecture'],  # type: ignore[index]
            output_file='ARCHITECTURE.md'
        )

    @task
    def ingest_project_doc(self) -> Task:
        return Task(
            config=self.tasks_config['ingest_project_doc'],  # type: ignore[index]
            output_file='PROJECT_SUMMARY.md'
        )

    @task
    def implement_backend(self) -> Task:
        return Task(
            config=self.tasks_config['implement_backend'],  # type: ignore[index]
        )

    @task
    def design_database(self) -> Task:
        return Task(
            config=self.tasks_config['design_database'],  # type: ignore[index]
        )

    @task
    def implement_client(self) -> Task:
        return Task(
            config=self.tasks_config['implement_client'],  # type: ignore[index]
        )

    @task
    def design_ux(self) -> Task:
        return Task(
            config=self.tasks_config['design_ux'],  # type: ignore[index]
        )

    @task
    def write_tests(self) -> Task:
        return Task(
            config=self.tasks_config['write_tests'],  # type: ignore[index]
        )

    @task
    def containerize_app(self) -> Task:
        return Task(
            config=self.tasks_config['containerize_app'],  # type: ignore[index]
        )

    @task
    def evaluate_and_feedback(self) -> Task:
        return Task(
            config=self.tasks_config['evaluate_and_feedback'],  # type: ignore[index]
            output_file='EVALUATION_REPORT.md'
        )

    @task
    def dynamic_features(self) -> Task:
        return Task(
            config=self.tasks_config['dynamic_features'],  # type: ignore[index]
        )

    @task
    def package_and_run(self) -> Task:
        return Task(
            config=self.tasks_config['package_and_run'],  # type: ignore[index]
            output_file='BUILD_AND_RUN.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SoftwareEngineer crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_agent=self.engineering_lead(),
            verbose=True,
        )
