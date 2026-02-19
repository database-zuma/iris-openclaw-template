"""
BM Deck Updater — Branch Configuration
Each branch: store names (exact match in DB), Vercel project alias, local HTML path
"""

import os

DB_URL = os.environ.get("DATABASE_URL", "postgresql://openclaw_app:Zuma-0psCl4w-2026!@76.13.194.120/openclaw_ops")
VERCEL_TOKEN = os.environ.get("VERCEL_TOKEN", "WNWvm9fjTerfhyG9zqiSEzdx")
VERCEL_BIN = os.path.expanduser("~/homebrew/Cellar/node/25.6.0/bin/node")
VERCEL_CLI = os.path.expanduser("~/homebrew/lib/node_modules/vercel/dist/index.js")

# Base path for BM deck HTML files
DECKS_BASE = os.path.expanduser(
    "~/.openclaw/workspace/zuma-bm-decks"
)

BRANCHES = {
    "jatim": {
        "label": "Jawa Timur",
        "vercel_alias": "zuma-bm-jatim.vercel.app",
        "deck_folder": os.path.join(DECKS_BASE, "bm-jatim"),
        "stores": [
            "zuma city of tomorrow mall",
            "zuma galaxy mall",
            "zuma icon gresik",
            "zuma lippo batu",
            "zuma lippo sidoarjo",
            "zuma mall olympic garden",
            "zuma matos",
            "zuma ptc",
            "zuma royal plaza",
            "zuma sunrise mall",
            "zuma tunjungan plaza",
        ],
        # FF/FA/FS uses different store names in mart.ff_fa_fs_daily
        "ff_store_map": {
            "zuma tunjungan plaza": "zuma tunjungan plaza 3",
            "zuma sunrise mall": "zuma sunrise mall mojokerto",
            "zuma icon gresik": "zuma icon mall gresik",
            "zuma galaxy mall": "zuma galaxy mall",
            "zuma city of tomorrow mall": "zuma city of tomorrow mall",
            "zuma mall olympic garden": "zuma mall olympic garden",
            "zuma matos": "zuma matos",
            "zuma royal plaza": "zuma royal plaza",
            "zuma lippo batu": "zuma lippo batu",
            "zuma lippo sidoarjo": "zuma lippo sidoarjo",
            "zuma ptc": "zuma ptc",
        },
        "target_branch": "Jawa Timur",
    },

    "bali": {
        "label": "Bali",
        "vercel_alias": "bm-bali.vercel.app",
        "deck_folder": os.path.join(DECKS_BASE, "bm-bali"),
        "stores": [
            "zuma bajra",
            "zuma bangli",
            "zuma batubulan",
            "zuma dalung",
            "zuma gianyar",
            "zuma icon bali",
            "zuma jembrana",
            "zuma kapal",
            "zuma karangasem",
            "zuma kedonganan",
            "zuma kesiman",
            "zuma klungkung",
            "zuma lebah peliatan",
            "zuma level 21",
            "zuma lippo bali",
            "zuma living world",
            "zuma mall bali galeria",
            "zuma monang maning",
            "zuma monkey forest ubud",
            "zuma panjer",
            "zuma peguyangan",
            "zuma peliatan",
            "zuma pemogan",
            "zuma penatih",
            "zuma seminyak village",
            "zuma seririt",
            "zuma singaraja",
            "zuma tabanan",
            "zuma tanah lot",
            "zuma tsm bali",
            "zuma uluwatu",
        ],
        "target_branch": "Bali",
    },

    "jakarta": {
        "label": "Jakarta",
        "vercel_alias": "bm-jakarta.vercel.app",
        "deck_folder": os.path.join(DECKS_BASE, "bm-jakarta"),
        "stores": [
            "zuma bintaro exchange",
            "zuma cinere bellevue mall",
            "zuma lippo mall puri",
            "zuma moi",
            "zuma pluit village",
        ],
        "target_branch": "Jakarta",
    },

    "lombok": {
        "label": "Lombok",
        "vercel_alias": "bm-lombok.vercel.app",
        "deck_folder": os.path.join(DECKS_BASE, "bm-lombok"),
        "stores": [
            "zuma epicentrum",
            "zuma mataram",
        ],
        "target_branch": "Lombok",
    },

    "sulawesi": {
        "label": "Sulawesi",
        "vercel_alias": "bm-sulawesi.vercel.app",
        "deck_folder": os.path.join(DECKS_BASE, "bm-sulawesi"),
        "stores": [
            "zuma mega mall",
        ],
        "target_branch": "Sulawesi",
    },

    "sumatra": {
        "label": "Sumatera",
        "vercel_alias": "zuma-bm-sumatra.vercel.app",
        "deck_folder": os.path.join(DECKS_BASE, "bm-sumatra"),
        "stores": [
            "zuma ska mall",
        ],
        "target_branch": "Sumatera",
    },

    "batam": {
        "label": "Batam",
        "vercel_alias": "zuma-bm-batam.vercel.app",
        "deck_folder": os.path.join(DECKS_BASE, "bm-batam"),
        "stores": [
            "zuma k square mall batam",
            "zuma nagoya hills",
        ],
        "target_branch": "Batam",  # Not in store_monthly_target 2026, targets will be 0
    },
}
