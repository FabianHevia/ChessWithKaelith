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
├── main.py                     
│
├── core/                       
│   ├── __init__.py
│   ├── app.py                  
│   ├── settings.py             
│   └── profile_manager.py      
│
├── ui/                         
│   ├── __init__.py
│   ├── components/             
│   │   ├── __init__.py
│   │   └── widgets.py          
│   │
│   ├── screens/                
│   │   ├── __init__.py
│   │   ├── base_screen.py      
│   │   ├── main_menu.py        
│   │   ├── profile_select.py   
│   │   ├── profile_create.py   
│   │   └── options_menu.py     
│   │
│   └── styles/                 
│       └── __init__.py
│
├── localization/               
│   ├── __init__.py
│   ├── i18n.py                 
│   ├── es.json                 
│   └── en.json                 
│
├── data/                       
│   ├── settings.json           
│   └── profiles.json           
│
└── assets/                     
    └── background.png          


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

