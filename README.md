# Library-DB
# Εργασία Ομάδας 31: Βάση Δεδομένων μιας Δανειστικής Βιβλιοθήκης

A small, local-library management project written in Python. This repository provides a simple UI and helper scripts to generate and populate a SQLite-based library database, manage members, and perform sign-in/login flows.

**Status:** Lightweight educational project — actively maintained by the repository owner.

**Contents**
- **Project:** Python-based library database manager with simple menus and DB generation scripts.
- **Main code:** library_db/
- **Database tools:** library_db/database_generation/

**Quick Start**

Prerequisites:
- Python 3.8+ installed on your machine.

1) Create and activate a virtual environment (Windows example):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) Install dependencies (the repository includes a dependency list at `library_db/dependences.txt`):

```powershell
pip install -r library_db/dependences.txt
```

3) Run the application (from repository root):

```powershell
python library_db/startUp.py
```

This starts the console/GUI menus for signing in and using the library interfaces.

Project layout (high level)
- `library_db/` — main application modules and UI scripts:
	- `startUp.py` — app entrypoint
	- `login_UI.py` — login user interface
	- `adminMenu.py`, `memberMenu.py`, `memberMenuSignIn.py` — menu modules
	- `memberMenuSQLite.py` — SQLite-backed member menu helpers
	- `dependences.txt` — dependency list (pip)
- `library_db/database_generation/` — helper scripts to build and populate the database:
	- `libraryDBGenerator.py`, `authorGeneration.py`, `bookGeneration.py`, `holdingGeneration.py`, `memberGeneration.py`, `positionGeneration.py`, etc.
	- `bookInfos.json` and other seed data

Database generation

The `database_generation` folder contains scripts to create and seed the SQLite database used by the app. To generate or reset the database, run the generator scripts directly, for example:

```powershell
python library_db/database_generation/libraryDBGenerator.py
```

Check the individual scripts for more granular generation options (authors, books, holdings, members).

Usage notes
- The app is designed to run locally and uses SQLite for storage.
- If any UI is platform-specific, prefer running from a regular terminal on Windows.

Development
- Run modules directly while in an activated virtual environment.
- Keep tests and changes small and focused; this repository is intended for learning and small utilities.

Dependencies
- See `library_db/dependences.txt` for the project's Python dependencies.