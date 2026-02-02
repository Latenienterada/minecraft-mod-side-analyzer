import zipfile
import json
from rules import CLIENT_KEYWORDS, SERVER_KEYWORDS, BOTH_KEYWORDS

def analyze_mod(jar_path):
    score = {"client": 0, "server": 0}

    with zipfile.ZipFile(jar_path, "r") as jar:
        files = jar.namelist()

        if "fabric.mod.json" in files:
            data = json.loads(jar.read("fabric.mod.json"))
            env = data.get("environment", "*")

            if env == "client":
                score["client"] += 40
            elif env == "server":
                score["server"] += 40
            else:
                score["client"] += 20
                score["server"] += 20

        if "META-INF/mods.toml" in files:
            text = jar.read("META-INF/mods.toml").decode(errors="ignore")

            if 'side="CLIENT"' in text:
                score["client"] += 40
            elif 'side="SERVER"' in text:
                score["server"] += 40
            elif 'side="BOTH"' in text:
                score["client"] += 20
                score["server"] += 20

        for file in files:
            for k in CLIENT_KEYWORDS:
                if k in file:
                    score["client"] += 1
            for k in SERVER_KEYWORDS:
                if k in file:
                    score["server"] += 1
            for k in BOTH_KEYWORDS:
                if k in file:
                    score["client"] += 1
                    score["server"] += 1

    total = score["client"] + score["server"]

    if total == 0:
        return {"side": "unknown", "confidence": 0, "scores": score}

    if abs(score["client"] - score["server"]) < 10:
        side = "both"
    elif score["client"] > score["server"]:
        side = "client"
    else:
        side = "server"

    confidence = round((max(score.values()) / total) * 100, 2)

    return {"side": side, "confidence": confidence, "scores": score}
