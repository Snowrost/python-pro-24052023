import sys
from unittest.mock import patch

import pytest

from lesson_2_hw.drunk_polish_calculator import main, op_plus


@pytest.mark.parametrize("x,y,expected_result", [(1, 1, 2), (0, 1, 1), (2, -1, 1)])
def test_op_plus(x: float, y: float, expected_result: float):
    # when
    result = op_plus(x, y)

    # then
    assert result == expected_result


@pytest.mark.parametrize(
    "expression,expected_result",
    [
        ("1 1 +", "2.0"),
        ("2 1 -", "1.0"),
        ("2 2 *", "4.0"),
        ("4 2 /", "2.0"),
        ("1 1 + 2 * 3 - 2 /", "0.5"),
    ],
)
def test_main(capsys, expression, expected_result):
    # when
    with patch("builtins.input", return_value=expression):
        main()

    # then
    assert capsys.readouterr().out.rstrip() == expected_result
