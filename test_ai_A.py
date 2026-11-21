import pytest
from load_scores import load_scores


def test_normal_input(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n"
        "Kim,90\n"
        "Lee,80\n"
        "Park,100\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == [("Kim", 90), ("Lee", 80), ("Park", 100)]
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


@pytest.mark.parametrize(
    "score",
    [-1, 0, 1, 99, 100, 101]
)
def test_score_boundary_values(tmp_path, score):
    file = tmp_path / "scores.csv"
    file.write_text(
        f"name,score\nKim,{score}\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    if 0 <= score <= 100:
        assert kept == [("Kim", score)]
        assert skipped == []
    else:
        assert kept == []
        assert skipped == [
            (2, f"Kim,{score}", "점수가 0~100 밖")
        ]


@pytest.mark.parametrize(
    "data, expected_reason",
    [
        ("Kim", "열 개수가 2가 아님"),
        ("Kim,90,extra", "열 개수가 2가 아님"),
        ("Kim,", "점수가 비어 있음"),
        ("Kim,abc", "점수가 정수가 아님"),
        ("Kim,90.5", "점수가 정수가 아님"),
        (",90", "이름이 비어 있음"),
    ]
)
def test_invalid_data(tmp_path, data, expected_reason):
    file = tmp_path / "scores.csv"
    file.write_text(
        f"name,score\n{data}\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == []
    assert skipped == [
        (2, data, expected_reason)
    ]


def test_duplicate_names_are_kept(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n"
        "Kim,90\n"
        "Lee,80\n"
        "Kim,70\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == [
        ("Kim", 90),
        ("Lee", 80),
        ("Kim", 70)
    ]
    assert skipped == []


def test_empty_lines_are_skipped_without_record(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n"
        "\n"
        "Kim,90\n"
        "\n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == [("Kim", 90)]
    assert skipped == []


def test_name_and_score_whitespace(tmp_path):
    file = tmp_path / "scores.csv"
    file.write_text(
        "name,score\n"
        "  Kim  , 90 \n",
        encoding="utf-8"
    )

    kept, skipped = load_scores(file)

    assert kept == [("Kim", 90)]
    assert skipped == []