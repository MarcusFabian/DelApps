"""Unit tests for the app duplicate remover module."""

from pathlib import Path
import sys


PROJECT_SRC = Path(__file__).resolve().parents[1] / "src"
if str(PROJECT_SRC) not in sys.path:
    sys.path.insert(0, str(PROJECT_SRC))

import app_duplicate_remover as remover


def test_parse_version_returns_tuple_of_integers() -> None:
    """Version strings should be converted into comparable tuples."""
    assert remover.parse_version("25.0.11.0") == (25, 0, 11, 0)


def test_parse_version_returns_lowest_version_for_invalid_input() -> None:
    """Invalid version strings should fall back to the lowest sortable value."""
    assert remover.parse_version("25.invalid.11") == (0,)


def test_extract_name_and_version_parses_expected_filename() -> None:
    """Valid app filenames should be split into name and version parts."""
    filename = "Microsoft_Base Application_25.0.23364.25858.app"
    assert remover.extract_name_and_version(filename) == (
        "Microsoft_Base Application",
        "25.0.23364.25858",
    )


def test_identify_files_to_delete_keeps_highest_version() -> None:
    """Only the lower versions of duplicate app files should be marked for deletion."""
    grouped_files = {
        "Microsoft_Base Application": [
            ("Microsoft_Base Application_24.0.0.0.app", "24.0.0.0"),
            ("Microsoft_Base Application_25.0.0.0.app", "25.0.0.0"),
            ("Microsoft_Base Application_23.5.0.0.app", "23.5.0.0"),
        ],
        "Single_App": [("Single_App_1.0.0.0.app", "1.0.0.0")],
    }

    files_to_delete = remover.identify_files_to_delete(grouped_files)

    assert files_to_delete == [
        "Microsoft_Base Application_24.0.0.0.app",
        "Microsoft_Base Application_23.5.0.0.app",
    ]


def test_delete_files_dry_run_leaves_files_in_place(tmp_path: Path) -> None:
    """Dry-run deletion should not remove any files from disk."""
    duplicate_file = tmp_path / "Example_App_1.0.0.0.app"
    duplicate_file.touch()

    remover.delete_files([duplicate_file.name], str(tmp_path), dry_run=True)

    assert duplicate_file.exists()


def test_main_deletes_older_duplicate_versions(tmp_path: Path, monkeypatch) -> None:
    """Running the remover in live mode should keep only the newest duplicate."""
    monkeypatch.chdir(tmp_path)

    older_file = tmp_path / "Example_App_1.0.0.0.app"
    newer_file = tmp_path / "Example_App_2.0.0.0.app"
    unrelated_file = tmp_path / "Another_App_1.0.0.0.app"

    older_file.touch()
    newer_file.touch()
    unrelated_file.touch()

    remover.main(directory=str(tmp_path), dry_run=False)

    assert not older_file.exists()
    assert newer_file.exists()
    assert unrelated_file.exists()