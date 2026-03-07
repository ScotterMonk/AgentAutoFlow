import queue
from types import SimpleNamespace

import main_gui


class _ButtonStub:
    def __init__(self):
        self.calls = []

    def config(self, **kwargs):
        self.calls.append(kwargs)


def test_load_favorite_folders_resets_screen_before_reloading(monkeypatch):
    """`Load Favorites` should clear old state before reloading the configured favorites."""
    ui_snapshots = []

    monkeypatch.setattr(main_gui.file_path_utils, "normalize_path", lambda p: p)
    monkeypatch.setattr(main_gui.file_path_utils, "ensure_roo_dir", lambda p: None)
    monkeypatch.setattr(main_gui.file_path_utils, "has_roo_dir", lambda p: True)

    dummy = SimpleNamespace(
        is_syncing=False,
        favorite_folders=["/fav-a", "/fav-b"],
        selected_folders=["/old-project"],
        planned_actions=[{"relative_path": "old.txt"}],
        event_queue=queue.Queue(),
        confirm_button=_ButtonStub(),
        delete_bak_button=_ButtonStub(),
        sync_button=_ButtonStub(),
        browse_button=_ButtonStub(),
    )

    dummy.event_queue.put("stale-event")
    dummy._update_folder_list_ui = lambda: ui_snapshots.append(list(dummy.selected_folders))
    dummy._reset_loaded_folder_state = lambda: main_gui.MainApp._reset_loaded_folder_state(dummy)

    main_gui.MainApp._load_favorite_folders(dummy)

    assert dummy.selected_folders == ["/fav-a", "/fav-b"]
    assert dummy.planned_actions == []
    assert dummy.is_syncing is False
    assert ui_snapshots == [[], ["/fav-a", "/fav-b"]]
    assert dummy.event_queue.empty() is True

    assert dummy.confirm_button.calls == [{"state": main_gui.tk.DISABLED}]
    assert dummy.delete_bak_button.calls == [{"state": main_gui.tk.DISABLED}]
    assert dummy.sync_button.calls == [{"state": main_gui.tk.NORMAL}]
    assert dummy.browse_button.calls == [{"state": main_gui.tk.NORMAL}]
