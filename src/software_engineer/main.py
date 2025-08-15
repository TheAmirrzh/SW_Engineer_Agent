import sys
import warnings
import os
from datetime import datetime
from pathlib import Path
import logging

from software_engineer.crew import SoftwareEngineer

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crew_execution.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def setup_project_environment():
    """Setup project environment and validate configuration"""
    
    logger.info("Setting up project environment...")
    
    # Create comprehensive output directory structure
    output_dirs = [
        'output',
        'output/documentation',
        'output/source',
        'output/source/shared/src/main/java/com/messenger/shared',
        'output/source/shared/src/test/java/com/messenger/shared',
        'output/source/server/src/main/java/com/messenger/server',
        'output/source/server/src/main/resources',
        'output/source/server/src/test/java/com/messenger/server',
        'output/source/client/src/main/java/com/messenger/client',
        'output/source/client/src/main/resources',
        'output/source/client/src/test/java/com/messenger/client',
        'output/database/migrations',
        'output/database/seed',
        'output/deployment/docker',
        'output/deployment/kubernetes',
        'output/deployment/scripts',
        'output/testing/unit',
        'output/testing/integration',
        'output/testing/e2e'
    ]
    
    for dir_path in output_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Created {len(output_dirs)} output directories")
    
    # Validate environment configuration
    required_env = ['GEMINI_API_KEY']
    missing_env = [var for var in required_env if not os.getenv(var)]
    
    if missing_env:
        logger.error(f"Missing required environment variables: {missing_env}")
        logger.error("Please set these in your .env file:")
        logger.error("GEMINI_API_KEY=your_gemini_api_key_here")
        return False
    
    # Check for optional configurations
    optional_configs = {
        'GEMINI_API_KEY': 'Enhanced backend agent capabilities',
        'PROJECT_PDF': 'Project requirements document',
        'CREW_TELEMETRY': 'CrewAI telemetry (set to false for privacy)',
        'SERPER_API_KEY': 'Serper API key for web search'
    }
    
    for var, description in optional_configs.items():
        value = os.getenv(var)
        if value:
            if var == 'PROJECT_PDF' and not os.path.exists(value):
                logger.warning(f"{var} file not found: {value}")
            else:
                logger.info(f"Found {var}: {description}")
        else:
            logger.info(f"Optional: {var} - {description}")
    
    return True


def load_user_context():
    """Load user context from knowledge base"""
    user_context = {}
    
    try:
        knowledge_file = Path('knowledge/user_preference.txt')
        if knowledge_file.exists():
            with open(knowledge_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                
            # Parse user preferences
            for line in content.split('\n'):
                line = line.strip()
                if ' is ' in line:
                    key, value = line.split(' is ', 1)
                    key = key.replace('User ', '').lower()
                    user_context[key] = value.rstrip('.')
                    
            logger.info(f"Loaded user context: {user_context}")
            
    except Exception as e:
        logger.warning(f"Could not load user context: {e}")
        user_context = {
            'name': 'Developer',
            'role': 'Software Engineer', 
            'location': 'Unknown',
            'interests': 'Software Development'
        }
        
    return user_context


def validate_crew_setup():
    """Validate that CrewAI setup is correct"""
    try:
        from crewai import __version__ as crewai_version
        logger.info(f"CrewAI version: {crewai_version}")
        
        # Test crew initialization
        crew_instance = SoftwareEngineer()
        logger.info("✅ Crew initialization successful")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Crew setup validation failed: {e}")
        return False


def run():
    """
    Execute the complete software engineering crew workflow
    """
    
    print("🚀 JAVA MESSENGER APP - SOFTWARE ENGINEERING CREW")
    print("=" * 60)
    
    logger.info("Starting Software Engineering Crew execution...")
    
    # Environment setup and validation
    if not setup_project_environment():
        logger.error("❌ Environment setup failed")
        return False
        
    if not validate_crew_setup():
        logger.error("❌ Crew validation failed")
        return False
    
    # Load user context
    user_context = load_user_context()
    
    # Comprehensive project inputs
    inputs = {
        # Core Project Definition
        'project_name': 'Telegram Clone Messenger Application',
        'project_type': 'Cross-platform Desktop Messaging Application',
        'project_description': '''
        A secure, real-time messaging application built with Java 21 and JavaFX 21.
        Features include user authentication, real-time chat, message history, 
        contact management, and cross-platform compatibility.
        ''',
        
        # Technical Specifications
        'tech_stack': {
            'backend': 'Java 21, Maven, Spring Boot/Javalin, WebSocket, SQLite/PostgreSQL',
            'frontend': 'JavaFX 21, FXML, CSS',
            'database': 'SQLite (dev), PostgreSQL (prod), Flyway migrations',
            'security': 'JWT, bcrypt, TLS/SSL',
            'build': 'Maven multi-module, Docker, CI/CD',
            'testing': 'JUnit 5, TestFX, Testcontainers, MockMvc'
        },
        
        'target_platforms': ['macOS 12+'], #'Windows 10/11' 'Ubuntu 20.04+'
        'java_version': '21',
        'javafx_version': '21',
        
        # User Context
        'user_name': user_context.get('name', 'Developer'),
        'user_role': user_context.get('role', 'Software Engineer'),
        'user_location': user_context.get('location', 'Unknown'),
        'user_expertise': user_context.get('interests', 'Software Development'),
        
        # Timeline and Resources
        'current_year': str(datetime.now().year),
        'project_timeline': '6-8 weeks',
        'development_approach': 'Agile with continuous integration',
        'team_composition': 'Full-stack developers with Java/JavaFX experience',
        
        # Core Requirements
        'functional_requirements': [
            'User registration and authentication system',
            'Real-time messaging with WebSocket communication',
            'Persistent message history with search capabilities',
            'Contact management and friend requests',
            'User presence indicators and typing notifications',
            'Message delivery and read receipts',
            'Offline message queuing and synchronization',
            'Cross-platform native installers'
        ],
        
        'non_functional_requirements': {
            'performance': 'Support 1000+ concurrent connections, <200ms message latency',
            'scalability': 'Horizontal scaling capability for backend services',
            'security': 'End-to-end encryption option, secure authentication',
            'usability': 'Intuitive UI following platform-specific conventions',
            'reliability': '99.5% uptime, graceful failure handling',
            'maintainability': 'Clean code, >80% test coverage, comprehensive documentation'
        },
        
        # Advanced Features (Phase 2)
        'advanced_features': [
            'File and media sharing',
            'Group messaging and channels',
            'Message reactions and threading',
            'Voice/video calling integration',
            'Mobile companion app',
            'Plugin/extension system',
            'Advanced search and filtering',
            'Themes and customization'
        ],
        
        # Quality Standards
        'quality_gates': {
            'code_coverage': '80% minimum',
            'security_scan': 'Zero high-severity vulnerabilities',
            'performance_test': 'Load test with 500 concurrent users',
            'ui_test': 'Cross-platform compatibility validation',
            'documentation': 'Complete API docs and user guides'
        },
        
        # Constraints and Assumptions
        'constraints': [
            'Use only Maven Central dependencies',
            'Maintain Java 21 compatibility',
            'Support offline functionality',
            'Memory usage <512MB for client app',
            'Database migrations must be reversible',
            'All code must pass security scanning'
        ],
        
        'assumptions': [
            'Users have Java 21+ installed or bundled JRE',
            'Network connectivity available for real-time features',
            'Standard desktop screen resolutions (1024x768+)',
            'Basic technical literacy for installation and usage'
        ]
    }
    
    try:
        # Log execution start
        start_time = datetime.now()
        logger.info(f"🚀 Crew execution started at {start_time}")
        logger.info(f"📋 Project: {inputs['project_name']}")
        logger.info(f"👤 User: {inputs['user_name']} ({inputs['user_role']})")
        
        # Initialize and execute crew
        logger.info("Initializing Software Engineering Crew...")
        software_crew = SoftwareEngineer()
        
        logger.info("Starting hierarchical crew execution...")
        result = software_crew.crew().kickoff(inputs=inputs)
        
        # Log execution completion
        end_time = datetime.now()
        execution_time = end_time - start_time
        
        logger.info("✅ Crew execution completed successfully!")
        logger.info(f"⏱️  Total execution time: {execution_time}")
        
        # Display results summary
        print("\n" + "="*80)
        print("🎉 PROJECT GENERATION COMPLETED SUCCESSFULLY!")
        print("="*80)
        print(f"📊 Execution Summary:")
        print(f"   ⏱️  Duration: {execution_time}")
        print(f"   📁 Output Directory: output/")
        print(f"   📋 Project: {inputs['project_name']}")
        print(f"   👤 Generated for: {inputs['user_name']}")
        print("\n📄 Generated Deliverables:")
        print("   ✅ REQUIREMENTS.md - Comprehensive requirements analysis")
        print("   ✅ ARCHITECTURE.md - Complete system architecture")
        print("   ✅ ARCHITECTURE_REVIEW.md - Quality gate validation")
        print("   ✅ DATABASE_DESIGN.md - Data layer architecture")
        print("   ✅ UX_DESIGN.md - User experience specifications")
        print("   ✅ Backend Implementation - Server-side code and APIs")
        print("   ✅ Frontend Implementation - JavaFX desktop application")
        print("   ✅ TESTING_STRATEGY.md - Comprehensive test suite")
        print("   ✅ IMPLEMENTATION_REVIEW.md - Quality validation")
        print("   ✅ DEPLOYMENT_GUIDE.md - Production deployment")
        print("   ✅ PROJECT_COMPLETION_REPORT.md - Final assessment")
        print("\n🚀 Next Steps:")
        print("   1. Review generated documentation in output/ directory")
        print("   2. Validate architecture and implementation approach")
        print("   3. Begin development following the generated roadmap")
        print("   4. Execute testing strategy and quality validation")
        print("   5. Deploy using provided deployment guides")
        print("="*80)
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Crew execution failed: {e}")
        logger.error("Check the logs above for detailed error information")
        print(f"\n❌ ERROR: {e}")
        print("Check crew_execution.log for detailed error information")
        raise


def train():
    """Train the crew for improved performance"""
    if len(sys.argv) < 3:
        print("Usage: train <n_iterations> <filename>")
        return
        
    n_iterations = int(sys.argv[1])
    filename = sys.argv[2]
    
    inputs = {
        "project_name": "Java Messenger Training",
        "current_year": str(datetime.now().year)
    }
    
    try:
        logger.info(f"Training crew for {n_iterations} iterations...")
        SoftwareEngineer().crew().train(
            n_iterations=n_iterations, 
            filename=filename, 
            inputs=inputs
        )
        logger.info("✅ Training completed successfully")
        
    except Exception as e:
        logger.error(f"❌ Training failed: {e}")
        raise


def replay():
    """Replay crew execution from a specific task"""
    if len(sys.argv) < 2:
        print("Usage: replay <task_id>")
        return
        
    task_id = sys.argv[1]
    
    try:
        logger.info(f"Replaying from task: {task_id}")
        SoftwareEngineer().crew().replay(task_id=task_id)
        logger.info("✅ Replay completed successfully")
        
    except Exception as e:
        logger.error(f"❌ Replay failed: {e}")
        raise


def test():
    """Test crew execution with evaluation"""
    if len(sys.argv) < 3:
        print("Usage: test <n_iterations> <eval_llm>")
        return
        
    n_iterations = int(sys.argv[1])
    eval_llm = sys.argv[2]
    
    inputs = {
        "project_name": "Java Messenger Test",
        "current_year": str(datetime.now().year)
    }
    
    try:
        logger.info(f"Testing crew for {n_iterations} iterations with {eval_llm}")
        SoftwareEngineer().crew().test(
            n_iterations=n_iterations, 
            eval_llm=eval_llm, 
            inputs=inputs
        )
        logger.info("✅ Testing completed successfully")
        
    except Exception as e:
        logger.error(f"❌ Testing failed: {e}")
        raise


if __name__ == "__main__":
    run()