from biocutils import setdiff


def test_setdiff_simple():
    assert setdiff() == []

    y = ["B", "C", "A", "D", "E"]
    out = setdiff(y)
    assert out == y

    out = setdiff(y, ["A", "C", "E"])
    assert out == ["B", "D"]

    out = setdiff(y, ["A", "C"], ["E"])
    assert out == ["B", "D"]


def test_setdiff_duplicates():
    # Deduplicates elements in the first sequence
    out = setdiff(["B", "B", "C", "A", "D", "D", "E"], ["A", "A", "F", "F"])
    assert out == ["B", "C", "D", "E"]

    out = setdiff(["B", "B", "C", "A", "D", "D", "E"], ["A", "A", "F", "F"], duplicate_method="last")
    assert out == ["B", "C", "D", "E"]

    # Switches the order of B being reported.
    out = setdiff(
        ["C", "A", "D", "B", "E", "B"], ["A", "C", "E", "F"], duplicate_method="last"
    )
    assert out == ["D", "B"]

    out = setdiff(
        ["C", "A", "D", "B", "E", "B"], ["A", "C", "E", "F"]
    )
    assert out == ["D", "B"]


def test_setdiff_none():
    y = ["B", None, "C", "A", None, "D", "E"]
    out = setdiff(y)
    assert out == ["B", "C", "A", "D", "E"]

    out = setdiff(y, ["A", None, "C"])
    assert out == ["B", "D", "E"]
