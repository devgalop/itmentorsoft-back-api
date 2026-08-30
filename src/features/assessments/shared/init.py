from fastapi import APIRouter

from src.features.assessments.get_question_by_id.get_question_by_id_endpoint import (
    router as get_question_by_id_router,
)
from src.features.assessments.get_questions_by_level.get_questions_by_level_endpoint import (
    router as get_questions_by_level_router,
)
from src.features.assessments.get_questions_by_category.get_questions_by_category_endpoint import (
    router as get_questions_by_category_router,
)
from src.features.assessments.register_question.register_question_endpoint import (
    router as register_question_router,
)
from src.features.assessments.update_question.update_question_endpoint import (
    router as update_question_router,
)
from src.features.assessments.get_assessment.get_assessment_endpoint import (
    router as get_assessment_router,
)
from src.features.assessments.save_assessments_answers.save_assessments_answers_endpoint import (
    router as save_assessment_answers_router,
)
from src.features.assessments.get_assessment_by_topic.get_assessment_by_topic_endpoint import (
    router as get_assessment_by_topic_router,
)
from src.features.assessments.get_question_categories.get_question_categories_endpoint import (
    router as get_question_categories_router,
)
from src.features.assessments.get_all_questions.get_all_questions_endpoint import (
    router as get_all_questions_router,
)
from src.features.assessments.get_pending_approval_questions.get_pending_approval_questions_endpoint import (
    router as get_pending_approval_questions_router,
)
from src.features.assessments.save_review_question.save_review_question_endpoint import (
    router as save_review_question_router,
)
from src.features.assessments.get_assessment_result.get_assessment_result_endpoint import (
    router as get_assessment_result_router,
)
from src.features.assessments.get_qualification_status.get_qualification_status_endpoint import (
    router as get_qualification_status_router,
)
from src.features.assessments.get_questions_topics.get_questions_topics_endpoint import (
    router as get_questions_topics_router,
)
from src.features.assessments.update_question_status.update_question_status_endpoint import (
    router as update_question_status_router,
)
from src.features.assessments.get_quantity_of_assessments.get_quantity_of_assessments_endpoint import (
    router as get_quantity_of_assessments_router,
)
from src.features.assessments.get_assessments_summary.get_assessments_summary_endpoint import (
    router as get_assessments_summary_router,
)
from src.features.assessments.get_available_models.get_available_models_endpoint import (
    router as get_available_models_router,
)
from src.features.assessments.get_model_selected.get_model_selected_endpoint import (
    router as get_model_selected_router,
)

router = APIRouter()
router.include_router(register_question_router)
router.include_router(get_question_by_id_router)
router.include_router(get_questions_by_level_router)
router.include_router(get_questions_by_category_router)
router.include_router(update_question_router)
router.include_router(get_assessment_router)
router.include_router(save_assessment_answers_router)
router.include_router(get_assessment_by_topic_router)
router.include_router(get_question_categories_router)
router.include_router(get_all_questions_router)
router.include_router(get_pending_approval_questions_router)
router.include_router(save_review_question_router)
router.include_router(get_assessment_result_router)
router.include_router(get_qualification_status_router)
router.include_router(get_questions_topics_router)
router.include_router(update_question_status_router)
router.include_router(get_quantity_of_assessments_router)
router.include_router(get_assessments_summary_router)
router.include_router(get_available_models_router)
router.include_router(get_model_selected_router)
