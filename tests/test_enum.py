from py_learning import TruncationStrategy


def test_enum() -> None:
    assert TruncationStrategy.ONLY_FIRST.value == "only_first"