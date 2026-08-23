from typing import Annotated
import uuid
from fastapi import Depends
from sqlalchemy import select
from datetime import datetime
import secrets
import os
from dotenv import load_dotenv
from src.features.user_management.shared.dependencies import get_password_hasher
from src.features.user_management.shared.password_hasher import PasswordHasher
from src.infrastructure.database.postgresql.models.postgresql_assessment_model import (
    AssessmentAnswerEntity,
    AssessmentEntity,
    AssessmentQuizEntity,
    ClassificationResultEntity,
    TopicResultEntity,
)
from src.infrastructure.database.postgresql.models.postgresql_content_rating import (
    ContentRating,
)
from src.infrastructure.database.postgresql.models.postgresql_question_model import (
    QuestionEntity,
)
from src.infrastructure.database.postgresql.models.postgresql_resource_content import (
    ResourceContentEntity,
)
from src.infrastructure.database.postgresql.models.postgresql_role_model import (
    RoleEntity,
)
from src.infrastructure.database.postgresql.shared.postgresql_database_session import (
    AsyncSessionLocal,
)
from src.infrastructure.database.postgresql.models.postgresql_user_model import (
    UserEntity,
)

load_dotenv()

ADMIN_USERNAME: str = os.getenv("DATABASE_ADMIN_USERNAME", "")
ADMIN_PASSWORD: str = os.getenv("DATABASE_ADMIN_PASSWORD", "")
ADMIN_EMAIL: str = os.getenv("DATABASE_ADMIN_EMAIL", "")

TEACHER_PASSWORD: str = os.getenv("DEFAULT_TEACHER_PASSWORD", "")
STUDENT_PASSWORD: str = os.getenv("DEFAULT_STUDENT_PASSWORD", "")


def check_env_variables():
    """Check if the required environment variables are set."""
    missing_vars: list[str] = []
    if not ADMIN_USERNAME:
        missing_vars.append("DATABASE_ADMIN_USERNAME")
    if not ADMIN_PASSWORD:
        missing_vars.append("DATABASE_ADMIN_PASSWORD")
    if not ADMIN_EMAIL:
        missing_vars.append("DATABASE_ADMIN_EMAIL")
    if not TEACHER_PASSWORD:
        missing_vars.append("DEFAULT_TEACHER_PASSWORD")
    if not STUDENT_PASSWORD:
        missing_vars.append("DEFAULT_STUDENT_PASSWORD")

    if missing_vars:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )


async def seed_database(
    password_hasher: Annotated[PasswordHasher, Depends(get_password_hasher)],
):
    async with AsyncSessionLocal() as session:
        check_env_variables()

        result = await session.execute(select(RoleEntity))
        roles = result.scalars().all()

        if roles:
            print("Database already seeded. Skipping seeding.")
            return

        role_admin = RoleEntity(
            id=uuid.uuid4().hex,
            name="admin",
            description="Administrator role with full permissions.",
        )
        session.add(role_admin)
        role_teacher = RoleEntity(
            id=uuid.uuid4().hex,
            name="teacher",
            description="Teacher role with permissions to manage courses and students.",
        )
        session.add(role_teacher)
        role_student = RoleEntity(
            id=uuid.uuid4().hex,
            name="student",
            description="Student role with permissions to access course materials.",
        )
        session.add(role_student)
        role_user = RoleEntity(
            id=uuid.uuid4().hex,
            name="user",
            description="Default user role with limited permissions.",
        )
        session.add(role_user)
        admin = UserEntity(
            id=uuid.uuid4().hex,
            username=ADMIN_USERNAME,
            email=ADMIN_EMAIL,
            hashed_password=password_hasher.hash_password(ADMIN_PASSWORD),
            status="active",
            role_id=role_admin.id,
        )
        session.add(admin)
        print("Admin user created")

        teacher = UserEntity(
            id=uuid.uuid4().hex,
            username="default_teacher",
            email="default_teacher@example.com",
            hashed_password=password_hasher.hash_password(TEACHER_PASSWORD),
            status="active",
            role_id=role_teacher.id,
        )
        session.add(teacher)
        print("Teacher user created")

        for i in range(1, 3):
            student = UserEntity(
                id=uuid.uuid4().hex,
                username=f"student{i}",
                email=f"student{i}@example.com",
                hashed_password=password_hasher.hash_password(STUDENT_PASSWORD),
                status="active",
                role_id=role_student.id,
            )
            session.add(student)
        print("Student users created")
        await session.commit()


async def seed_assessments():
    async with AsyncSessionLocal() as session:
        student_summaries_result = await session.execute(
            select(TopicResultEntity).limit(1)
        )
        student_summaries = student_summaries_result.scalars().all()
        if student_summaries:
            print("assessments already seeded. Skipping seeding.")
            return

        result = await session.execute(
            select(UserEntity).where(UserEntity.username.contains("student"))
        )
        students = result.scalars().all()

        questions_result = await session.execute(select(QuestionEntity).limit(20))

        topics_result = await session.execute(
            select(QuestionEntity.classification).distinct()
        )
        questions = questions_result.scalars().all()
        topics = topics_result.scalars().all()

        questions_by_assessment = [
            questions[i : i + 5] for i in range(0, len(questions), 5)
        ]

        for student in students:
            for i, question_set in enumerate(questions_by_assessment):
                assessment_id = uuid.uuid4().hex
                assessment = AssessmentEntity(
                    id=assessment_id, user_id=student.id, created_at=datetime.now()
                )
                session.add(assessment)

                classification_result = ClassificationResultEntity(
                    user_id=student.id,
                    assessment_id=assessment_id,
                    classification="básico",
                    feedback="Sample feedback for the student's performance.",
                    is_enabled=True if i == len(questions_by_assessment) - 1 else False,
                )
                session.add(classification_result)
                print(
                    f"Assessment {i} created for student {student.username} with classification result {classification_result.classification}"
                )

                assessment_answers: list[AssessmentAnswerEntity] = []
                assessment_quizzes: list[AssessmentQuizEntity] = []
                for question in question_set:
                    assessment_quiz = AssessmentQuizEntity(
                        assessment_id=assessment_id,
                        question_id=question.id,
                        created_at=datetime.now(),
                    )
                    assessment_quizzes.append(assessment_quiz)
                    assessment_answer = AssessmentAnswerEntity(
                        id=uuid.uuid4().hex,
                        assessment_id=assessment_id,
                        question_id=question.id,
                        answer=f"Sample answer for question {question.id}",
                        time_taken_seconds=30,
                    )
                    assessment_answers.append(assessment_answer)
                session.add_all(assessment_answers)
                session.add_all(assessment_quizzes)
                print(
                    f"Assessment {i} created for student {student.username} with {len(assessment_answers)} answers"
                )

            number_of_grades = 4
            for idx in range(4):
                is_enabled = False
                if idx == number_of_grades - 1:
                    is_enabled = True
                for topic in topics:
                    random_score = secrets.randbelow(4)
                    topic_result = TopicResultEntity(
                        user_id=student.id,
                        topic=topic,
                        score=random_score,
                        is_enabled=is_enabled,
                    )
                    session.add(topic_result)
                print(
                    f"Knowledge profile created for student {student.username} with status {is_enabled}"
                )

        await session.commit()


async def seed_contents():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(ResourceContentEntity))
        contents = result.scalars().all()

        if contents:
            print("Contents already seeded. Skipping seeding.")
            return
        topics_result = await session.execute(
            select(QuestionEntity.classification).distinct()
        )
        topics = topics_result.scalars().all()
        students = await session.execute(
            select(UserEntity).where(UserEntity.username.contains("student"))
        )
        students = students.scalars().all()
        contents = []
        ratings = []
        for topic in topics:
            for i in range(1, 30):
                content_id = uuid.uuid4().hex
                content = ResourceContentEntity(
                    id=content_id,
                    title=f"Sample Content {i}",
                    summary=f"This is a description for Sample Content {i}.",
                    category="básico" if i % 2 == 0 else "intermedio",
                    url=f"https://example.com/content/{i}",
                    related_topics=f"{topic}",
                )
                contents.append(content)
                rating = ContentRating(
                    id=uuid.uuid4().hex,
                    content_id=content_id,
                    user_id=students[i % len(students)].id,
                    rating=secrets.randbelow(5) + 1,
                )
                ratings.append(rating)
            print(f"Sample contents created for topic {topic}")
        session.add_all(contents)
        session.add_all(ratings)
        print("Sample contents created")
        await session.commit()
