from .service import LlmService


class LlmDependencies:

    @staticmethod
    def get_llm_service():
        return LlmService
