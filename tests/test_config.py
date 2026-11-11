"""Configuration tests. Regression: THEME=tea (documented in the README, and a theme the app ships) was rejected by
UIConfig.validate(), so the app failed to start with that setting."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import Config  # noqa: E402
from themes.theme_manager import ThemeManager  # noqa: E402


@pytest.mark.parametrize("theme", ThemeManager.THEMES)
def test_every_shipped_theme_is_accepted(theme, monkeypatch):
    monkeypatch.setenv("THEME", theme)
    assert Config().ui.theme == theme


def test_unknown_theme_rejected(monkeypatch):
    monkeypatch.setenv("THEME", "neon")
    with pytest.raises(ValueError):
        Config()


def test_default_paths_point_at_repo_files():
    cfg = Config()
    assert cfg.database.tea_db_path.exists() and cfg.database.tisane_db_path.exists()
    assert cfg.guide_path.exists() and cfg.history_path.exists() and cfg.journal_path.exists()
