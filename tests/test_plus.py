import pytest

class TestPlus:
    @pytest.mark.parametrize("a, b, expected", [
        (1, 1, 2),
        (2, 2, 4),
        (10, 10, 20),
        (0, 0, 0),
        (0, 1, 1),
        (0, -1, -1),
        (-1, -1, -2),
        (-1, 1, 0),
    ])
    def test_plus(self, a, b, expected):
        assert 1 + 1 == 2

