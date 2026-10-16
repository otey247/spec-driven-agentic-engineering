"""Run local-only demo: REVIEWFLOW_DEMO_MODE=1 python -m reviewflow"""
from __future__ import annotations

import os
from pathlib import Path

import uvicorn

from .api import create_app


def main() -> None:
    if os.getenv("REVIEWFLOW_DEMO_MODE") != "1":
        raise SystemExit(
            "Demo credentials are disabled by default. "
            "Set REVIEWFLOW_DEMO_MODE=1 for a local-only training server."
        )
    db_path = Path(os.getenv("REVIEWFLOW_DB", ".data/reviewflow.db"))
    app = create_app(db_path, demo_mode=True)
    print("Local training server: http://127.0.0.1:8000 (do not expose externally)")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")


if __name__ == "__main__":
    main()
