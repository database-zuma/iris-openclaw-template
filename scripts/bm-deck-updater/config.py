"""
BM Deck Updater — Branch Configuration
Each branch: store names (exact match in DB), Vercel project alias, local HTML path
"""

import os

DB_URL = os.environ.get("DATABASE_URL", "postgresql://openclaw_app:Zuma-0psCl4w-2026!@76.13.194.120/openclaw_ops")
VERCEL_TOKEN = os.environ.get("VERCEL_TOKEN", "WNWvm9fjTerfhyG9zqiSEzdx")
VERCEL_BIN = os.path.expanduser("~/homebrew/Cellar/node/25.6.0/bin/node")
VERCEL_CLI = os.path.expanduser("~/homebrew/lib/node_modules/vercel/dist/index.js")

# Base path for deck HTML files
DECKS_BASE = os.path.expanduser(
    "~/.openclaw/workspace/zuma-business-skills/references/decks"
)

BRANCHES = {
    "jatim": {
        "label": "Jawa Timur",
        "vercel_alias": "zuma-bm-jatim.vercel.app",
        "deck_folder": os.path.join(DECKS_BASE, "bm-jatim"),
        "stores": [
            "zuma lippo sidoarjo",
            "zuma ptc",
            "zuma tunjungan plaza",
            "zuma mall olympic garden",
            "zuma olympic garden",
            "zuma lippo batu",
            "zuma matos",
            "zuma royal plaza",
            "zuma sunrise mall",
            "zuma icon gresik",
            "zuma galaxy mall",
            "zuma city of tomorrow",
        ],
        "target_branch": "Jawa Timur",
    },
    # Future branches — add when deck is created
    # "bali": {
    #     "label": "Bali",
    #     "vercel_alias": "zuma-bm-bali.vercel.app",
    #     "deck_folder": os.path.join(DECKS_BASE, "bm-bali"),
    #     "stores": [...],
    #     "target_branch": "Bali",
    # },
}
