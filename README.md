# ♟️ Chess with Kaelith

Desktop application for the chess game “Chess with Kaelith”, developed in Python using Tkinter.

  - A mythological chess experience beyond the board
  - Chess with Kaelith is a reimagined chess application that blends classical strategy with mythological narrative and immersive presentation.
  - The core gameplay remains faithful to traditional chess rules, but the experience is elevated through lore-driven progression, symbolic factions, and a cinematic interface designed for desktop environments.
  

## 🌌 Lore & Narrative
In the world of Kaelith, chess is not merely a game — it is a ritual of balance.Each match represents a confrontation between ancient forces embodied as mythological archetypes. Pieces are no longer abstract tokens, but avatars of forgotten orders, celestial hierarchies, or fallen civilizations.
  
The player does not simply “play”, but aligns with philosophies, memories, and destinies that unfold as the game progresses.


## 🎮 Design Philosophy
- Board-first clarity: The chessboard stays readable and classical.
- Narrative outside the board: Lore, characters, and environments live around it.
- Desktop-oriented UX: Designed for PC, not scaled-up mobile UI.
- Respect for chess tradition: No rule-breaking gimmicks.
- This project aims to sit somewhere between:
- A chess engine, a mythological art piece, and an interactive codex.

## 📁 Project Architecture
chess_with_kaelith/
│
├── main.py                     # Application entry point
│
├── core/                       # Core application logic
│   ├── __init__.py
│   ├── app.py                  # Main controller (window, navigation)
│   ├── settings.py             # Settings manager (JSON)
│   └── profile_manager.py      # Player profile manager (JSON)
│
├── ui/                         # User interface
│   ├── __init__.py
│   ├── components/             # Reusable UI components
│   │   ├── __init__.py
│   │   └── widgets.py          # Custom buttons, sliders, entries
│   │
│   ├── screens/                # Application screens
│   │   ├── __init__.py
│   │   ├── base_screen.py      # Base class for screens
│   │   ├── main_menu.py        # Main menu
│   │   ├── profile_select.py   # Profile selection
│   │   ├── profile_create.py   # Profile creation
│   │   └── options_menu.py     # Options menu
│   │
│   └── styles/                 # Styles and themes (future)
│       └── __init__.py
│
├── localization/               # Localization system
│   ├── __init__.py
│   ├── i18n.py                 # Translation manager
│   ├── es.json                 # Spanish translations (optional)
│   └── en.json                 # English translations (optional)
│
├── data/                       # Persistent data (generated at runtime)
│   ├── settings.json           # Saved settings
│   └── profiles.json           # Player profiles
│
└── assets/                     # Graphic assets
    └── background.png          # Background image

## 🔄 Screen Flow Diagram
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                    🏠 MAIN MENU                                 │
│                    ────────────                                 │
│                                                                 │
│    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐       │
│    │   PLAY      │    │  OPTIONS    │    │    EXIT     │       │
│    │  (Primary)  │    │ (Secondary) │    │ (Secondary) │       │
│    └──────┬──────┘    └──────┬──────┘    └─────────────┘       │
│           │                  │                                  │
│           │                  │     ┌────────────────────────┐   │
│           │                  │     │  🌐 Language Selector  │   │
│           │                  │     │  ES 🇪🇸 | EN 🇬🇧        │   │
│           │                  │     └────────────────────────┘   │
│           │                  │     ┌────────────────────────┐   │
│           │                  │     │  🔊 Volume Control     │   │
│           │                  │     │  ████████░░ 80%        │   │
│           │                  │     └────────────────────────┘   │
│           │                  │                                  │
└───────────┼──────────────────┼──────────────────────────────────┘
            │                  │
            ▼                  ▼
┌───────────────────┐  ┌─────────────────────────────────────────┐
│                   │  │                                         │
│ 👤 PROFILE SELECT │  │  ⚙️ OPTIONS MENU                        │
│ ─────────────────│  │  ──────────────                         │
│                   │  │                                         │
│ ┌───────────────┐ │  │  ┌─────┬─────┬─────────────┐           │
│ │ 🎮 Profile 1  │ │  │  │Video│Sound│Accessibility│  TABS     │
│ │ Level 5       │──┼──│  └─────┴─────┴─────────────┘           │
│ │ 23 matches    │ │  │                                         │
│ └───────────────┘ │  │  ┌─────────────────────────┐           │
│                   │  │  │ • Fullscreen            │           │
│ ┌───────────────┐ │  │  │ • Resolution            │           │
│ │ 🎮 Profile 2  │ │  │  │ • Master volume         │           │
│ │ Level 2       │ │  │  │ • Music / Effects       │           │
│ │ 8 matches     │ │  │  │ • Text size             │           │
│ └───────────────┘ │  │  │ • High contrast         │           │
│                   │  │  └─────────────────────────┘           │
│ [+ Create Profile]│  │                                         │
│     [Back]        │  │  [Reset]              [Back]           │
│                   │  │                                         │
└─────────┬─────────┘  └─────────────────────────────────────────┘
          │
          ▼
┌───────────────────┐
│                   │
│ ✨ PROFILE CREATE │
│ ─────────────────│
│                   │
│  ┌─────────────┐  │
│  │  Nickname   │  │
│  │ [________]  │  │
│  └─────────────┘  │
│                   │
│  [Create] [Cancel]│
│                   │
└───────────────────┘

## 🎨 Color Palette
| Usage               | Color Name      | Hex       |
| ------------------- | --------------- | --------- |
| Primary buttons     | Forest green    | `#4a6741` |
| Active states       | Light green     | `#6b8b5e` |
| Borders / accents   | Earth brown     | `#8b7355` |
| Secondary text      | Gold / Beige    | `#c4a574` |
| Titles / highlights | Light text      | `#f5f0e6` |
| Main text           | Dark background | `#1a2318` |


## 🚧 Project Status

This is an evolving project under active development.
Expect experimentation, iteration, and gradual expansion of features and lore.

