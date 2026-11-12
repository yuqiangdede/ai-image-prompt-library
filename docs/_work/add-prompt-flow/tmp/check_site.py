"""Static checks for site/index.html and site/app.js."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
html = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
js = (ROOT / "site" / "app.js").read_text(encoding="utf-8")

ids = re.findall(r'\bid="([^"]+)"', html)
duplicates = sorted({value for value in ids if ids.count(value) > 1})
assert not duplicates, duplicates

id_set = set(ids)
missing = sorted({value for value in re.findall(r'\$\("([^"]+)"\)', js) if value not in id_set})
assert not missing, missing

for attribute in ("for", "aria-controls", "aria-labelledby", "aria-describedby"):
    targets = re.findall(r'\b' + attribute + r'="([^"]+)"', html)
    for target in targets:
        if " " in target or not target:
            continue
        assert target in id_set, (attribute, target)

assert html.count("<main") == 1 and html.count("</main>") == 1
assert html.count("<body") == 1 and html.count("</body>") == 1
print("site references: ok,", len(ids), "ids")
