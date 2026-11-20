import os
import time
import urllib.request

# QUARTO_DOCUMENT_PATH er selve mappen med .qmd-filen (ikke filstien)
skabelon_mappe = os.path.abspath(
    os.environ.get("QUARTO_DOCUMENT_PATH") or os.getcwd()
)

FILER = [globals().get("ku_skabelon.tex"), "KU_logo.png"]

# True = ignorer lokale kopier og hent seneste version fra GitHub
opdater = globals().get("OPDATER", False)

for navn in FILER:
    dest = os.path.join(skabelon_mappe, navn)
    lokal_findes = os.path.exists(dest)
    if lokal_findes and not opdater:
        print(f"Bruger lokal kopi af {navn}")
        continue
    url = f"{base_url}/{navn}"
    if url.startswith("http"):
        url += f"?t={int(time.time())}"  # sikrer nyeste version (omgår cache)
    tmp = dest + ".download"
    try:
        urllib.request.urlretrieve(url, tmp)
        os.replace(tmp, dest)
        print(f"{navn} hentet fra GitHub")
    except Exception as e:
        if os.path.exists(tmp):
            os.remove(tmp)
        if lokal_findes:
            print(f"Kunne ikke opdatere {navn} ({e}) - bruger lokal kopi")
            continue
        raise SystemExit(
            f"Ingen lokal kopi af {navn} - og kan ikke hente fra GitHub: {e}"
        )
