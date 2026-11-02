"""Espelha no Facebook (Pagina Cristo em Nos) os posts de imagem novos do @cristoemnoscelioleme.
Roda junto com o publicador. Registro em status/espelho.json."""
import json, os, sys, datetime, urllib.request, urllib.parse, uuid

G = "https://graph.facebook.com/v21.0"
TOKEN = os.environ["META_TOKEN"]
IG = "17841444466812805"
PAGE = "1336827002856846"
DESDE = os.environ.get("ESPELHO_DESDE", "2026-11-02T00:30:00+0000")
TESTE = os.environ.get("ESPELHO_TESTE") == "1"
REG = "status/espelho.json"

def get(path, **p):
    p["access_token"] = p.pop("token", TOKEN)
    with urllib.request.urlopen(f"{G}/{path}?{urllib.parse.urlencode(p)}", timeout=60) as r:
        return json.loads(r.read())

def foto_fb(pt, img, legenda, publicar=True):
    b = uuid.uuid4().hex
    campos = {"caption": legenda, "access_token": pt, "published": "true" if publicar else "false"}
    corpo = b""
    for k, v in campos.items():
        corpo += f"--{b}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
    corpo += f"--{b}\r\nContent-Disposition: form-data; name=\"source\"; filename=\"img.jpg\"\r\nContent-Type: image/jpeg\r\n\r\n".encode() + img + f"\r\n--{b}--\r\n".encode()
    req = urllib.request.Request(f"{G}/{PAGE}/photos", data=corpo, method="POST",
                                 headers={"Content-Type": f"multipart/form-data; boundary={b}"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read() or b"{}")

def main():
    reg = json.load(open(REG)) if os.path.exists(REG) else {}
    pt = get(PAGE, fields="access_token")["access_token"]
    posts = get(f"{IG}/media", fields="id,caption,media_type,media_url,timestamp,permalink", limit=15)["data"]
    mudou = False
    for p in reversed(posts):
        if p["id"] in reg or p["timestamp"] < DESDE:
            continue
        if p["media_type"] != "IMAGE":
            reg[p["id"]] = {"ignorado": p["media_type"], "permalink": p.get("permalink")}
            mudou = True
            continue
        with urllib.request.urlopen(p["media_url"], timeout=60) as r:
            img = r.read()
        res = foto_fb(pt, img, p.get("caption", ""), publicar=not TESTE)
        print(p["permalink"], res, flush=True)
        if res.get("id"):
            reg[p["id"]] = {"fb": res.get("post_id") or res["id"], "permalink": p.get("permalink"),
                            "teste": TESTE, "em": datetime.datetime.utcnow().isoformat() + "Z"}
            mudou = True
        if TESTE:
            break
    if mudou:
        os.makedirs("status", exist_ok=True)
        json.dump(reg, open(REG, "w"), ensure_ascii=False, indent=1)
    return mudou

if __name__ == "__main__":
    main()
