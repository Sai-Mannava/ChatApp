from app.services.ai import AIWriterService


def test_generate_contains_tone_and_prompt():
    service = AIWriterService()
    result = service.generate("Launch our beta in May", "confident")
    assert "Confident Draft" in result
    assert "Launch our beta in May" in result


def test_refine_compacts_whitespace():
    service = AIWriterService()
    result = service.refine("This   is   spaced\n\nout")
    assert "This is spaced out" in result
