from textwrap import dedent


class AIWriterService:
    """Pluggable AI service.

    This default implementation is deterministic and low-latency so the
    application runs locally without external model dependencies.
    """

    def generate(self, prompt: str, tone: str) -> str:
        return dedent(
            f"""
            [{tone.title()} Draft]
            {prompt.strip()}

            Key message:
            - Start with a clear objective.
            - Support with one concrete example.
            - End with a concise call to action.
            """
        ).strip()

    def edit(self, text: str, instruction: str) -> str:
        return dedent(
            f"""
            [Edited per instruction: {instruction.strip()}]
            {text.strip()}
            """
        ).strip()

    def refine(self, text: str) -> str:
        cleaned = " ".join(text.split())
        return dedent(
            f"""
            [Refined Version]
            {cleaned}

            Improvements made:
            - Reduced redundancy.
            - Improved sentence flow.
            - Preserved original intent.
            """
        ).strip()
