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


def test_setdiff_factor():
    from biocutils import Factor
    f1 = Factor.from_sequence(["B", "B", "C", "A", "D", "D", "E"])
    f2 = Factor.from_sequence(["A", "A", "F", "F"])

    out = setdiff(f1, f2)
    assert isinstance(out, Factor)
    assert out.as_list() == ["B", "C", "D", "E"]
    assert out.get_levels() == f1.get_levels()

    out = setdiff(f1, f2, duplicate_method="last")
    assert isinstance(out, Factor)
    assert out.as_list() == ["B", "C", "D", "E"]
    assert out.get_levels() == f1.get_levels()

    f3 = Factor.from_sequence(["C", "A", "D", "B", "E", "B"])
    f4 = Factor.from_sequence(["A", "C", "E", "F"])
    out = setdiff(f3, f4, duplicate_method="last")
    assert isinstance(out, Factor)
    assert out.as_list() == ["D", "B"]
    assert out.get_levels() == f3.get_levels()

    out = setdiff(f3, f4)
    assert isinstance(out, Factor)
    assert out.as_list() == ["D", "B"]
    assert out.get_levels() == f3.get_levels()
