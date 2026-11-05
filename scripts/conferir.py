"""Conferencia diaria do post das 22h (Brasilia). Roda dentro do workflow; so age entre 01:20Z e 03:00Z.
Confere feed e story no IG (CEN e celioleme) e na Pagina; se faltar story, publica a partir do item da fila do dia.
Grava status/conferencia-AAAA-MM-DD.json (data de Brasilia)."""
import json, os, glob, datetime, subprocess, urllib.request, urllib.parse
G = "https://graph.facebook.com/v21.0"; TOKEN = os.environ["META_TOKEN"]; REPO = os.environ.get("GITHUB_REPOSITORY", "")
IG = {"cristoemnoscelioleme": "17841444466812805", "celioleme": "17841401087933569"}
PAGE = "1336827002856846"
def api(m, p, **k):
    k.setdefault("access_token", TOKEN); d = urllib.parse.urlencode(k).encode()
    r = urllib.request.Request(f"{G}/{p}" + ("?" + d.decode() if m == "GET" else ""), data=None if m == "GET" else d, method=m)
    try: return json.loads(urllib.request.urlopen(r, timeout=120).read())
    except urllib.error.HTTPError as e: return json.loads(e.read() or b"{}")
def ts(s): return datetime.datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")
agora = datetime.datetime.utcnow()
if not (agora.hour == 1 and agora.minute >= 20 or agora.hour == 2): raise SystemExit
dia = (agora - datetime.timedelta(hours=3)).date()          # data de Brasilia do post
desde = datetime.datetime.combine(dia + datetime.timedelta(days=1), datetime.time(0, 50))  # 21h50 BRT
arq = f"status/conferencia-{dia}.json"
if os.path.exists(arq): raise SystemExit
rel = {"dia": str(dia), "verificado_utc": agora.isoformat() + "Z", "itens": {}, "correcoes": []}
for nome, i in IG.items():
    feed = [m for m in api("GET", f"{i}/media", fields="timestamp", limit=5).get("data", []) if ts(m["timestamp"]) >= desde]
    st = [m for m in api("GET", f"{i}/stories", fields="timestamp,media_type,permalink").get("data", []) if ts(m["timestamp"]) >= desde]
    rel["itens"][f"ig_{nome}_feed"] = bool(feed); rel["itens"][f"ig_{nome}_story"] = bool(st)
    # a esteira nunca publica story em video: video em story = repost indevido (ex.: Reel republicado)
    vid = [{"hora": m["timestamp"], "link": m.get("permalink", "")} for m in st if m.get("media_type") == "VIDEO"]
    if vid: rel.setdefault("alertas", []).append({f"ig_{nome}_story_video_inesperado": vid})
pt = api("GET", PAGE, fields="access_token")["access_token"]
pf = [p for p in api("GET", f"{PAGE}/posts", fields="created_time", limit=5, access_token=pt).get("data", []) if ts(p["created_time"]) >= desde]
ps = [s for s in api("GET", f"{PAGE}/stories", access_token=pt).get("data", []) if datetime.datetime.utcfromtimestamp(int(s["creation_time"])) >= desde]
rel["itens"]["fb_pagina_feed"] = bool(pf); rel["itens"]["fb_pagina_story"] = bool(ps)
# story de origem: item da fila publicado/vencido nesta janela que tenha story
origem = None
for pj in sorted(glob.glob("fila/*/post*.json")):
    p = json.load(open(pj)); q = ts(p["publicar_em_utc"].replace("Z", ""))
    if desde <= q <= agora and os.path.exists(os.path.dirname(pj) + "/story.jpg.enc") and not pj.endswith("pulado.json"):
        origem = os.path.dirname(pj); break
if origem is None:  # dias do Business Suite: usa a reserva do dia
    r = glob.glob(f"fila/reserva-{dia}-*/story.jpg.enc"); origem = os.path.dirname(r[0]) if r else None
rel["origem_story"] = origem
def story_url():
    os.makedirs("tmp", exist_ok=True); t = f"tmp/conf_{dia}.jpg"
    subprocess.run(["openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2", "-pass", "env:META_TOKEN", "-in", origem + "/story.jpg.enc", "-out", t], check=True)
    subprocess.run(["git", "add", t]); subprocess.run(["git", "commit", "-qm", f"tmp conf {dia}"]); subprocess.run(["git", "push", "-q"])
    import time; time.sleep(15); return t, f"https://raw.githubusercontent.com/{REPO}/main/{t}"
tmp = None
if origem:
    if not rel["itens"]["fb_pagina_story"]:
        tmp, url = story_url()
        f = api("POST", f"{PAGE}/photos", url=url, published="false", access_token=pt)
        r = api("POST", f"{PAGE}/photo_stories", photo_id=f.get("id", ""), access_token=pt) if f.get("id") else f
        rel["correcoes"].append({"fb_pagina_story": r})
    for nome, i in IG.items():
        if rel["itens"][f"ig_{nome}_feed"] and not rel["itens"][f"ig_{nome}_story"]:
            if not tmp: tmp, url = story_url()
            c = api("POST", f"{i}/media", media_type="STORIES", image_url=url)
            import time
            for _ in range(24):
                time.sleep(5)
                if api("GET", c.get("id", "x"), fields="status_code").get("status_code") in ("FINISHED", "ERROR"): break
            rel["correcoes"].append({f"ig_{nome}_story": api("POST", f"{i}/media_publish", creation_id=c.get("id", ""))})
if tmp:
    subprocess.run(["git", "rm", "-q", tmp]); subprocess.run(["git", "commit", "-qm", f"remove tmp conf {dia}"])
rel["ok"] = (all(rel["itens"].values()) or bool(rel["correcoes"])) and not rel.get("alertas")
os.makedirs("status", exist_ok=True); json.dump(rel, open(arq, "w"), ensure_ascii=False, indent=1)
subprocess.run(["git", "pull", "-q", "--rebase"]); subprocess.run(["git", "add", arq])
subprocess.run(["git", "commit", "-qm", f"conferencia {dia}"]); subprocess.run(["git", "push", "-q"])
print(json.dumps(rel, ensure_ascii=False))
