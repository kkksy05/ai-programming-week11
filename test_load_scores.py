
import csv
import pytest

from load_scores import load_scores


def make_csv(tmp_path, rows):
    """테스트용 CSV 파일을 만든다."""
    path = tmp_path / "test.csv"

    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    return path


def test_normal_file(tmp_path):
    """정상적인 성적과 이름에 쉼표가 있는 경우."""
    path = make_csv(tmp_path, [
        ["name", "score"],
        ["홍길동", "90"],
        ["김,철수", "80"],
        [],
    ])

    kept, skipped = load_scores(path)

    assert kept == [("홍길동", 90), ("김,철수", 80)]
    assert skipped == []


def test_header_only(tmp_path):
    """헤더만 있는 파일은 빈 목록을 반환한다."""
    path = make_csv(tmp_path, [["name", "score"]])

    kept, skipped = load_scores(path)

    assert kept == []
    assert skipped == []


def test_file_not_found(tmp_path):
    """존재하지 않는 파일은 오류가 발생한다."""
    path = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_scores(path)


@pytest.mark.parametrize(
    "score, is_valid",
    [
        ("-1", False),
        ("0", True),
        ("1", True),
        ("99", True),
        ("100", True),
        ("101", False),
    ],
)
def test_score_boundary(tmp_path, score, is_valid):
    """점수의 경계값을 확인한다."""
    path = make_csv(tmp_path, [
        ["name", "score"],
        ["학생", score],
    ])

    kept, skipped = load_scores(path)

    if is_valid:
        assert kept == [("학생", int(score))]
        assert skipped == []
    else:
        assert kept == []
        assert len(skipped) == 1


def test_invalid_rows(tmp_path):
    """잘못된 데이터는 건너뛰고 기록한다."""
    path = make_csv(tmp_path, [
        ["name", "score"],
        ["홍길동"],
        ["김철수", ""],
        ["이영희", "abc"],
        ["", "80"],
    ])

    kept, skipped = load_scores(path)

    assert kept == []
    assert len(skipped) == 4


def test_duplicate_names(tmp_path):
    """같은 이름이 있어도 모두 남긴다."""
    path = make_csv(tmp_path, [
        ["name", "score"],
        ["홍길동", "90"],
        ["홍길동", "80"],
    ])

    kept, skipped = load_scores(path)

    assert kept == [("홍길동", 90), ("홍길동", 80)]
    assert skipped == []
