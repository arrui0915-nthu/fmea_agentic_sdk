from src.demo_questions import SAMPLE_QUESTIONS


def test_demo_questions_are_complete_prompts_without_rpn_qualifier() -> None:
    assert len(SAMPLE_QUESTIONS) == 6
    assert all(question.endswith(("？", "。")) for question in SAMPLE_QUESTIONS)
    assert any("沒有" not in question and "Particle high" in question for question in SAMPLE_QUESTIONS)
    assert "請計算各製程的平均 RPN，並依平均 RPN 由高到低排序。" in SAMPLE_QUESTIONS
    assert all("改善前" not in question for question in SAMPLE_QUESTIONS)
