class WriterGuardrail:
    @staticmethod
    def validate(content: str | None) -> str:
        if not content:
            raise ValueError(
                "The Writer Agent did not produce a response."
            )

        cleaned_content = content.strip()

        if not cleaned_content:
            raise ValueError(
                "The Writer Agent produced an empty response."
            )

        return cleaned_content