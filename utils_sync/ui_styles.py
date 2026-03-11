"""TTK dark-theme style configuration for AgentAutoFlow."""

import tkinter as tk
from tkinter import ttk


def apply_dark_theme(style: ttk.Style, config: dict) -> None:
    """Configure all AF.* TTK styles for the dark theme.
    
    Args:
        style: The ttk.Style instance to configure.
        config: The application config dict for color/font keys.
    """
    try:
        style.theme_use("clam")
    except tk.TclError:
        # Fall back to current theme if clam is unavailable
        pass

    # Dark background for frames and labels
    style.configure("TFrame", background=config["ui_dark_bg"])
    style.configure("TLabel", background=config["ui_dark_bg"], foreground=config["ui_fg_primary"])

    # Base button style (fallback)
    style.configure(
        "TButton",
        background=config["ui_button_bg"],
        foreground=config["ui_button_text"],
    )

    # Primary app button style: black background, green outline, hover highlight
    style.configure(
        "AF.TButton",
        background=config["ui_button_bg"],
        foreground=config["ui_button_text"],
        bordercolor=config["ui_button_border"],
        focusthickness=1,
        focuscolor=config["ui_button_border"],
    )
    style.map(
        "AF.TButton",
        background=[("active", config["ui_button_bg_hover"])],
        bordercolor=[("active", config["ui_button_border"])],
        foreground=[
            ("active", config["ui_button_border"]),
            ("disabled", "#555555"),
        ],
    )

    # Danger style (for destructive actions like Delete .bak)
    style.configure(
        "AFDanger.TButton",
        background=config["ui_button_bg"],
        foreground="#ff6666",
        bordercolor="#ff6666",
        focusthickness=1,
        focuscolor="#ff6666",
    )
    style.map(
        "AFDanger.TButton",
        background=[("active", config["ui_button_bg_hover"])],
        bordercolor=[("active", "#ff6666")],
        foreground=[
            ("active", config["ui_button_border"]),
            ("disabled", "#555555"),
        ],
    )

    # Compact button style for small icon buttons (used in folder rows)
    style.configure(
        "AFMini.TButton",
        background=config["ui_button_bg"],
        foreground=config["ui_button_text"],
        bordercolor=config["ui_button_border"],
        focusthickness=1,
        focuscolor=config["ui_button_border"],
        padding=0,
    )
    style.map(
        "AFMini.TButton",
        background=[("active", config["ui_button_bg_hover"])],
        bordercolor=[("active", config["ui_button_border"])],
    )

    # Compact danger button style for file delete buttons (red X)
    style.configure(
        "AFDangerMini.TButton",
        background=config["ui_button_bg"],
        foreground="#ff6666",
        bordercolor="#ff6666",
        focusthickness=1,
        focuscolor="#ff6666",
        padding=0,
    )
    style.map(
        "AFDangerMini.TButton",
        background=[("active", config["ui_button_bg_hover"])],
        bordercolor=[("active", "#ff6666")],
        foreground=[("active", "#ff8888")],
    )

    # Progress bar style: dark, invisible trough with a glowing green bar
    # The trough matches the dark bg so idle (0%) bars visually disappear,
    # while the active portion uses the same neon green as primary actions.
    #
    # Progressbar internally prefixes the style with "Horizontal." for horizontal
    # bars, so a Progressbar with style="AF.Progressbar" will actually look for
    # the layout/style "Horizontal.AF.Progressbar". We clone the base horizontal
    # layout and then customize colors so Tk has a valid layout for this style.
    style.layout("Horizontal.AF.Progressbar", style.layout("Horizontal.TProgressbar"))
    style.configure(
        "Horizontal.AF.Progressbar",
        troughcolor=config["ui_dark_bg"],
        background=config["ui_button_border"],
        bordercolor=config["ui_button_border"],
        lightcolor="#66ff99",
        darkcolor=config["ui_button_border"],
        thickness=8,
    )

    # Scrollbar style: subtle dark theme: very dark grey trough, deep muted green thumb
    style.configure(
        "Vertical.TScrollbar",
        troughcolor="#151515",        # darker than ui_dark_bg_alt but not pure black
        background="#0f3b24",        # deep, low-saturation green thumb
        bordercolor="#0f3b24",
        arrowcolor="#666666",        # neutral arrows so the thumb doesn't pop
    )
    style.map(
        "Vertical.TScrollbar",
        background=[("active", "#145232")],  # slightly lighter but still dark green on hover
    )
