from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.features.assessments.evaluate.evaluate_assessment_handler import (
    EvaluateAssessmentHandler,
)
from src.features.assessments.evaluate.evaluate_assessment_service import (
    EvaluateAssessmentService,
)
from src.features.assessments.shared.questions_seeder import seed_questions
from src.features.user_management.shared.init import router as user_management_router
from src.features.content_management.shared.init import (
    router as content_management_router,
)
from src.features.assessments.shared.init import router as assessments_router
from src.features.reports.shared.init import router as reports_router
from src.infrastructure.database.postgresql.shared.postgresql_database_session import (
    init_db,
)
from src.infrastructure.database.postgresql.shared.postgresql_seeder import (
    seed_assessments,
    seed_contents,
    seed_database,
)
from src.infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher
from src.infrastructure.broker.aws.services.aws_sqs_manager import SqsManagerService
from src.infrastructure.env_manager.env_manager import EnvironmentVariablesConstants


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up the application...")
    print("Validating mandatory environment variables...")
    EnvironmentVariablesConstants.validate_mandatory_env_vars()
    print("Initializing the database...")
    await init_db()
    await seed_database(BcryptPasswordHasher())
    await seed_questions()
    await seed_assessments()
    await seed_contents()
    print("Application startup complete.")
    print("Starting the SQS consumer services...")
    evaluate_contract = EvaluateAssessmentHandler(EvaluateAssessmentService())
    sqs_manager_service = SqsManagerService(evaluate_contract=evaluate_contract)
    sqs_manager_service.create_queues()
    consumers = sqs_manager_service.start_consumer_services()
    yield
    print("Shutting down the application...")
    await sqs_manager_service.stop_consumer_services(consumers)
    print("Application shutdown complete.")


app = FastAPI(lifespan=lifespan)

app.include_router(user_management_router, prefix="/users", tags=["Users"])
app.include_router(content_management_router, prefix="/content", tags=["Content"])
app.include_router(assessments_router, prefix="/assessments", tags=["Assessments"])
app.include_router(reports_router, prefix="/reports", tags=["Reports"])
