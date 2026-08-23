class ContentByTopic:
    def __init__(self, content_id: str, title: str, description: str, rating: float):
        self.content_id = content_id
        self.title = title
        self.description = description
        self.rating = rating


class LearningPath:
    def __init__(
        self,
        path_id: str,
        user_id: str,
        topic: str,
        is_completed: bool,
        contents: list[ContentByTopic],
    ):
        self.path_id = path_id
        self.user_id = user_id
        self.topic = topic
        self.is_completed = is_completed
        self.contents = contents


class LearningPathResponse:
    def __init__(
        self, is_success: bool, message: str, recommendation: list[LearningPath]
    ):
        self.is_success = is_success
        self.message = message
        self.recommendation = recommendation


class LearningPathProgress:
    def __init__(self, path_id: str, progress: float):
        self.path_id = path_id
        self.progress = progress


class LearningPathProgressResponse:
    def __init__(
        self, is_success: bool, message: str, path_progress: LearningPathProgress | None
    ):
        self.is_success = is_success
        self.message = message
        self.path_progress = path_progress
