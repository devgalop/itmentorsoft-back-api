from itmentorsoft_persistence.dto import Assessment


class EvaluateAssessmentRequest:
    def __init__(self, assessment: Assessment):
        self.assessment = assessment
