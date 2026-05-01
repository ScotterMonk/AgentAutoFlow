from pathlib import Path
from types import SimpleNamespace

import main_gui
from utils_sync import settings_window


def test_text_values_join_handles_path_objects():
    joined = settings_window._text_values_join([Path("project_a"), "project_b", "  "])

    assert joined == "project_a, project_b"


def test_folders_faves_text_parse_accepts_commas_and_newlines():
    raw_text = "C:/project-a/app,\nC:/project-b/app\nC:/project-c/app, C:/project-d/app\n\n"

    parsed = settings_window._folders_faves_text_parse(raw_text)

    assert parsed == [
        "C:/project-a/app",
        "C:/project-b/app",
        "C:/project-c/app",
        "C:/project-d/app",
    ]


def test_save_favorites_to_config_serializes_paths(monkeypatch):
    saved_configs = []

    def _save_config_stub(config_dict):
        saved_configs.append(dict(config_dict))
        return True

    monkeypatch.setattr(main_gui.config_sync, "save_config", _save_config_stub)

    dummy = SimpleNamespace(
        config={},
        favorite_folders=[Path("project_a"), Path("project_b")],
    )

    main_gui.MainApp._save_favorites_to_config(dummy)

    assert dummy.config["folders_faves"] == ["project_a", "project_b"]
    assert saved_configs[0]["folders_faves"] == ["project_a", "project_b"]
