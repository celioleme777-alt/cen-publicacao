"""Confere, a cada execucao, se TODAS as partes de story em video publicadas nas ultimas 22 h
continuam no ar em cada conta do Instagram. Parte que sumiu e republicada uma unica vez.
Registro: status/partes-<id>.json (o que foi visto, o que faltou, o que foi republicado)."""
import json, os, re, glob, time, datetime, subprocess, urllib.request, urllib.parse
G = "https://graph.facebook.com/v21.0"; TOKEN = os.environ["META_TOKEN"]; REPO = os.environ.get("GITHUB_REPOSITORY", "")
IG = {"cristoemnoscelioleme": "17841444466812805", "celioleme": "17841401087933569",
      "celiolemeoficial": "17841463128497736"}
SECO = os.environ.get("SECO") == "1"   # SECO=1: so confere, nao publica nada
def api(m, p, **k):
    k.setdefault("access_token", TOKEN); d = urllib.parse.urlencode(k).encode()
    r = urllib.request.Request(f"{G}/{p}" + ("?" + d.decode() if m == "GET" else ""), data=None if m == "GET" else d, method=m)
    try: return json.loads(urllib.request.urlopen(r, timeout=120).read())
    except urllib.error.HTTPError as e: return json.loads(e.read() or b"{}")
agora = datetime.datetime.utcnow()
no_ar = {}
def stories(nome):
    if nome not in no_ar:
        no_ar[nome] = {m["id"] for m in api("GET", f"{IG[nome]}/stories", fields="id").get("data", [])}
    return no_ar[nome]
PADRAO = re.compile(r"story video IG (\w+) publicado: \{'id': '(\d+)'\}")
relatorio = []
for f in sorted(glob.glob("status/*.json")):
    pid = os.path.basename(f)[:-5]
    if pid.startswith(("partes-", "conferencia-", "fbstory-")) or pid == "espelho": continue
    try: st = json.load(open(f))
    except Exception: continue
    if not isinstance(st, dict) or not st.get("fim"): continue
    fim = datetime.datetime.strptime(st["fim"][:19], "%Y-%m-%dT%H:%M:%S")
    if not (datetime.timedelta(minutes=15) <= agora - fim <= datetime.timedelta(hours=22)): continue
    # ids publicados, em ordem, por conta (parte 1, parte 2...)
    pub = {}
    for e in st.get("etapas", []):
        m = PADRAO.search(str(e))
        if m and m.group(1) in IG: pub.setdefault(m.group(1), []).append(m.group(2))
    if not pub: continue
    arq = f"status/partes-{pid}.json"
    reg = json.load(open(arq)) if os.path.exists(arq) else {"id": pid, "republicado": {}, "verificacoes": []}
    falta = {n: [k + 1 for k, i in enumerate(ids) if i not in stories(n)] for n, ids in pub.items()}
    falta = {n: v for n, v in falta.items() if v}
    reg["verificacoes"] = (reg["verificacoes"] + [{"utc": agora.isoformat() + "Z", "faltando": falta}])[-20:]
    pasta = f"fila/{pid}"
    partes = sorted(glob.glob(f"{pasta}/story_p*.mp4.enc")) or sorted(glob.glob(f"{pasta}/story.mp4.enc"))
    for nome, ks in falta.items():
        for k in ks:
            chave = f"{nome}#{k}"
            if chave in reg["republicado"] or SECO or k > len(partes): continue
            os.makedirs("tmp", exist_ok=True); t = f"tmp/partes_{pid}_{k}.mp4"
            subprocess.run(["openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2", "-pass", "env:META_TOKEN",
                            "-in", partes[k - 1], "-out", t], check=True)
            subprocess.run(["git", "add", t]); subprocess.run(["git", "commit", "-qm", f"tmp {t}"])
            subprocess.run(["git", "pull", "-q", "--rebase"]); subprocess.run(["git", "push", "-q"]); time.sleep(15)
            c = api("POST", f"{IG[nome]}/media", media_type="STORIES", video_url=f"https://raw.githubusercontent.com/{REPO}/main/{t}")
            for _ in range(60):
                time.sleep(5)
                if api("GET", c.get("id", "x"), fields="status_code").get("status_code") in ("FINISHED", "ERROR"): break
            r = api("POST", f"{IG[nome]}/media_publish", creation_id=c.get("id", ""))
            reg["republicado"][chave] = {"utc": datetime.datetime.utcnow().isoformat() + "Z", "resultado": r}
            subprocess.run(["git", "rm", "-q", t]); subprocess.run(["git", "commit", "-qm", f"remove {t}"])
    relatorio.append({pid: falta})
    if not SECO:
        json.dump(reg, open(arq, "w"), ensure_ascii=False, indent=1)
        subprocess.run(["git", "add", arq])
if not SECO:
    subprocess.run(["git", "commit", "-qm", "conferencia de partes de story"], capture_output=True)
    subprocess.run(["git", "pull", "-q", "--rebase"]); subprocess.run(["git", "push", "-q"])
print(json.dumps(relatorio, ensure_ascii=False))
