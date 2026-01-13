"""AgentAutoFlow File Sync - GUI entrypoint wrapper.

This project historically launched the GUI via `main_gui.py`.
`app.py` exists purely for consistency with other applications and simply
executes `main_gui.py` as if it were run directly.
"""

import runpy


def main() -> None:
    """Launch the Tkinter GUI defined in `main_gui.py`."""
    runpy.run_module("main_gui", run_name="__main__")


if __name__ == "__main__":
    main()

