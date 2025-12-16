[⬅️ Back to Main README](../README.md)

# ⚡ uv: Modern Python Package Management

## 1. Architectural Decision Record
Traditional Python package management (`pip`, `virtualenv`) often conflicts with modern operating system protections. Specifically, **PEP 668** restricts system-wide `pip` usage to prevent destabilizing the OS.

We selected **`uv`** for this project to provide:
1.  **System Isolation:** `uv` operates independently of the system Python, bypassing PEP 668 restrictions safely.
2.  **Performance:** Written in Rust, it resolves and installs dependencies 10-100x faster than standard tools.
3.  **Unified Toolchain:** It manages python versions, virtual environments, and dependencies in a single binary.

---

## 2. Installation Guide

To avoid conflicts with system package managers (`apt`, `yum`, `brew`), install `uv` via its standalone installer.

**Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

*After installation, you may need to restart your terminal or source your profile (`source ~/.bashrc`) to access the `uv` command.*

---

## 3. Operational Workflow

`uv` simplifies the execution pipeline into single, atomic commands. It automatically creates and manages the virtual environment for you.

### Step 1: Execution
To run a script, simply prepend `uv run`. The tool checks `pyproject.toml`, ensures the environment is sync'd, and executes the code.

```bash
uv run feature_extractor.py
```

### Step 2: Adding Dependencies
If you need to extend the project (e.g., adding `pandas`):

```bash
uv add pandas
```
This updates `pyproject.toml` and the lockfile instantly.

---

## 4. Troubleshooting

### Issue: "Permission denied (os error 13)"
**Context:** This error occurs when `uv` attempts to write to the `.venv` directory but lacks ownership. This typically happens if you previously ran the project using **Docker** or **sudo**, creating root-owned files in your workspace.
**Resolution:** Reclaim ownership of the project directory.
```bash
sudo chown -R $USER:$USER .
```

### Issue: "The virtual environment was not created... ensurepip is not available"
**Context:** On minimal Linux installations (like WSL or Ubuntu Server), the standard Python venv module might be stripped to save space.
**Resolution:** Install the `venv` module explicitly.
```bash
sudo apt install python3-venv  # Or python3.12-venv depending on your version
```