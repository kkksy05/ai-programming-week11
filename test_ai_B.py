import pytest
from load_scores import load_scores


def test_normal_input(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text("name,score\nKim,90\nLee,80\nPark,70\n", encoding="utf-8")

    kept, skipped = load_scores(file)

    assert kept == [("Kim", 90), ("Lee", 80), ("Park", 70)]
    assert skipped == []


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_scores("not_exist.csv")


def test_header_only(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text("name,score\n", encoding="utf-8")

    kept, skipped = load_scores(file)

    assert kept == []
    assert skipped == []


def test_wrong_number_of_columns(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\nKim,90,extra\nLee\nPark,80\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == [("Park", 80)]
    assert len(skipped) == 2


def test_empty_or_non_integer_score(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\nKim,\nLee,abc\nPark,85.5\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == []
    assert len(skipped) == 3


@pytest.mark.parametrize(
    "score, expected",
    [
        (-1, False),
        (0, True),
        (1, True),
        (99, True),
        (100, True),
        (101, False),
    ]
)
def test_score_boundary_values(tmp_path, score, expected):
    file = tmp_path / "scores.csv"
    file.write_text(
        f"name,score\nKim,{score}\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    if expected:
        assert kept == [("Kim", score)]
        assert skipped == []
    else:
        assert kept == []
        assert len(skipped) == 1


def test_empty_name(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text("name,score\n,90\n", encoding="utf-8")

    kept, skipped = load_scores(file)

    assert kept == []
    assert len(skipped) == 1


def test_duplicate_names_are_kept(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\nKim,90\nLee,80\nKim,70\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == [("Kim", 90), ("Lee", 80), ("Kim", 70)]
    assert skipped == []


def test_empty_lines_are_skipped_without_record(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n\nKim,90\n\nLee,80\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == [("Kim", 90), ("Lee", 80)]
    assert skipped == []


def test_skipped_records_contain_line_number_original_line_and_reason(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\nKim,150\nLee,abc\n,80\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == []
    assert len(skipped) == 3

    assert skipped[0][0] == 2
    assert skipped[0][1] == "Kim,150"
    assert skipped[0][2]

    assert skipped[1][0] == 3
    assert skipped[1][1] == "Lee,abc"
    assert skipped[1][2]

    assert skipped[2][0] == 4
    assert skipped[2][1] == ",80"
    assert skipped[2][2]