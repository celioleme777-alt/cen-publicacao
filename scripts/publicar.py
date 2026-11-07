"""Publicador CEN: publica itens da fila (fila/<id>/post.json) quando chega a hora.
Segredo necessario: META_TOKEN (token do usuario do sistema publicador-cen)."""
import json, os, sys, time, subprocess, glob, datetime, urllib.request, urllib.parse

G = "https://graph.facebook.com/v21.0"
TOKEN = os.environ["META_TOKEN"]
REPO = os.environ["GITHUB_REPOSITORY"]
IG = {"cristoemnoscelioleme": "17841444466812805", "celioleme": "17841401087933569",
      "celiolemeoficial": "17841463128497736"}
PAGE = "1336827002856846"

def api(method, path, **params):
    params["access_token"] = params.pop("token", TOKEN)
    data = urllib.parse.urlencode(params).encode()
    url = f"{G}/{path}"
    if method == "GET":
        req = urllib.request.Request(url + "?" + data.decode())
    else:
        req = urllib.request.Request(url, data=data, method=method)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read() or b"{}")

def git(*a):
    if a[0] == "push":
        subprocess.run(["git", "pull", "-q", "--rebase"], check=True)
    subprocess.run(["git", *a], check=True)

def salvar_status(pid, st):
    os.makedirs("status", exist_ok=True)
    json.dump(st, open(f"status/{pid}.json", "w"), ensure_ascii=False, indent=1)

def publicar(pasta):
    post = json.load(open(f"{pasta}/post.json"))
    if len(post.get("legenda", "")) > 2200:  # limite do Instagram
        raise ValueError(f"legenda com {len(post['legenda'])} caracteres (limite 2200)")
    if post.get("tipo") == "imagem":
        return publicar_imagem(pasta, post)
    if post.get("tipo") == "story_video":
        return publicar_story_video(pasta, post)
    return publicar_reel(pasta, post)

def tmp_publico(pid, nome_enc, ext):
    """Decifra um arquivo da fila e o publica temporariamente no repositorio (URL publica)."""
    os.makedirs("tmp", exist_ok=True)
    tmp = f"tmp/{pid}_{nome_enc.split('.')[0]}.{ext}"
    subprocess.run(["openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2", "-pass", "env:META_TOKEN",
                    "-in", f"fila/{pid}/{nome_enc}", "-out", tmp], check=True)
    return tmp, f"https://raw.githubusercontent.com/{REPO}/main/{tmp}"

def esperar(cid, log, tentativas=60):
    estado = {}
    for _ in range(tentativas):
        time.sleep(5)
        estado = api("GET", cid, fields="status_code,status")
        if estado.get("status_code") in ("FINISHED", "ERROR"):
            break
    log(f"processamento: {estado}")
    return estado.get("status_code") == "FINISHED"

def aceitar_convites(mid, colaboradores, log):
    for nome in colaboradores:
        for _ in range(18):
            time.sleep(10)
            inv = api("GET", f"{IG[nome]}/collaboration_invites")
            if any(i.get("media_id") == mid for i in inv.get("data", [])):
                log(f"convite aceito em {nome}: {api('POST', f'{IG[nome]}/collaboration_invites', media_id=mid, accept='true')}")
                break
        else:
            log(f"convite NAO encontrado em {nome}")

def stories_video(urls, nomes, facebook, log, teste=False):
    """Publica videos (partes em ordem) como stories no IG (contas em nomes) e na Pagina do Facebook."""
    if isinstance(urls, str): urls = [urls]
    for url in urls:
        _story_video(url, nomes, facebook, log, teste)
        time.sleep(15)

def _story_video(url, nomes, facebook, log, teste=False):
    for nome in nomes:
        c = api("POST", f"{IG[nome]}/media", media_type="STORIES", video_url=url)
        log(f"container story video IG {nome}: {c}")
        if c.get("id") and esperar(c["id"], log, tentativas=120):
            if teste:
                log(f"TESTE: story video IG {nome} pronto")
            else:
                log(f"story video IG {nome} publicado: {api('POST', f'{IG[nome]}/media_publish', creation_id=c['id'])}")
        else:
            log(f"ERRO story video IG {nome}")
    if facebook and not teste:
        pt = api("GET", PAGE, fields="access_token")["access_token"]
        s = api("POST", f"{PAGE}/video_stories", upload_phase="start", token=pt)
        log(f"story video FB start: {s}")
        if s.get("video_id"):
            req = urllib.request.Request(s["upload_url"], method="POST",
                                         headers={"Authorization": f"OAuth {pt}", "file_url": url})
            with urllib.request.urlopen(req, timeout=300) as r:
                log(f"upload story FB: {r.read().decode()}")
            time.sleep(20)
            log(f"story video FB: {api('POST', f'{PAGE}/video_stories', upload_phase='finish', video_id=s['video_id'], token=pt)}")

def partes_story(pasta):
    """story_p1.mp4.enc, story_p2.mp4.enc... (em ordem) ou story.mp4.enc."""
    p = sorted(glob.glob(f"{pasta}/story_p*.mp4.enc"))
    return p or ([f"{pasta}/story.mp4.enc"] if os.path.exists(f"{pasta}/story.mp4.enc") else [])

def publicar_story_video(pasta, post):
    pid = os.path.basename(pasta)
    st = {"id": pid, "tipo": "story_video", "inicio": datetime.datetime.utcnow().isoformat() + "Z", "etapas": []}
    log = lambda m: (st["etapas"].append(m), print(m, flush=True))
    pares = [tmp_publico(pid, os.path.basename(f), "mp4") for f in partes_story(pasta)]
    git("add", *[t for t, _ in pares]); git("commit", "-qm", f"tmp {pid}"); git("push", "-q")
    time.sleep(10)
    try:
        stories_video([u for _, u in pares], post.get("stories_em", ["cristoemnoscelioleme", "celioleme"]),
                      post.get("facebook", True), log, post.get("teste", False))
    finally:
        git("rm", "-q", *[t for t, _ in pares]); git("commit", "-qm", f"remove tmp {pid}"); git("push", "-q")
    st["fim"] = datetime.datetime.utcnow().isoformat() + "Z"
    salvar_status(pid, st)
    os.rename(f"{pasta}/post.json", f"{pasta}/post.feito.json")
    git("add", "-A", "status", pasta); git("commit", "-qm", f"status {pid}"); git("push", "-q")

def publicar_imagem(pasta, post):
    pid = os.path.basename(pasta)
    st = {"id": pid, "tipo": "imagem", "inicio": datetime.datetime.utcnow().isoformat() + "Z", "etapas": []}
    log = lambda m: (st["etapas"].append(m), print(m, flush=True))
    teste = post.get("teste", False)
    ig = IG[post.get("conta", "cristoemnoscelioleme")]
    tmps = []
    feed_url = None
    if os.path.exists(f"{pasta}/feed.jpg.enc") and post.get("feed", True):
        feed_tmp, feed_url = tmp_publico(pid, "feed.jpg.enc", "jpg"); tmps.append(feed_tmp)
    story_url = None
    if os.path.exists(f"{pasta}/story.jpg.enc"):
        story_tmp, story_url = tmp_publico(pid, "story.jpg.enc", "jpg"); tmps.append(story_tmp)
    git("add", *tmps); git("commit", "-qm", f"tmp {pid}"); git("push", "-q")
    time.sleep(10)
    try:
        # 1. Feed do Instagram (o espelho leva ao Facebook)
        if feed_url:
            p = dict(image_url=feed_url, caption=post["legenda"])
            if post.get("colaboradores"):
                p["collaborators"] = json.dumps(post["colaboradores"])
            c = api("POST", f"{ig}/media", **p)
            log(f"container feed IG: {c}")
            if c.get("id") and esperar(c["id"], log):
                if teste:
                    log("TESTE: feed IG pronto, nao publicado")
                else:
                    pub = api("POST", f"{ig}/media_publish", creation_id=c["id"])
                    log(f"feed IG publicado: {pub}")
                    if pub.get("id"):
                        st["permalink_ig"] = api("GET", pub["id"], fields="permalink").get("permalink")
                        aceitar_convites(pub["id"], post.get("colaboradores", []), log)
            else:
                st["erro"] = "feed IG nao ficou pronto"
        # 2. Stories do Instagram (conta principal + contas listadas em stories_em)
        if story_url and post.get("story", True):
            for nome in post.get("stories_em", ["cristoemnoscelioleme"]):
                c = api("POST", f"{IG[nome]}/media", media_type="STORIES", image_url=story_url)
                log(f"container story IG {nome}: {c}")
                if c.get("id") and esperar(c["id"], log):
                    if teste:
                        log(f"TESTE: story IG {nome} pronto, nao publicado")
                    else:
                        log(f"story IG {nome} publicado: {api('POST', f'{IG[nome]}/media_publish', creation_id=c['id'])}")
                else:
                    st[f"erro_story_ig_{nome}"] = "story IG nao ficou pronto"
        # 3. Story da Pagina do Facebook
        if story_url and post.get("story", True) and post.get("facebook", True) and not teste:
            pt = api("GET", PAGE, fields="access_token")["access_token"]
            foto = api("POST", f"{PAGE}/photos", url=story_url, published="false", token=pt)
            log(f"foto story FB: {foto}")
            if foto.get("id"):
                log(f"story FB: {api('POST', f'{PAGE}/photo_stories', photo_id=foto['id'], token=pt)}")
    finally:
        git("rm", "-q", *tmps); git("commit", "-qm", f"remove tmp {pid}"); git("push", "-q")
        log("arquivos temporarios removidos")
    st["fim"] = datetime.datetime.utcnow().isoformat() + "Z"
    salvar_status(pid, st)
    os.rename(f"{pasta}/post.json", f"{pasta}/post.feito.json")
    git("add", "-A", "status", pasta); git("commit", "-qm", f"status {pid}"); git("push", "-q")

def publicar_reel(pasta, post):
    pid = os.path.basename(pasta)
    st = {"id": pid, "inicio": datetime.datetime.utcnow().isoformat() + "Z", "etapas": []}
    log = lambda m: (st["etapas"].append(m), print(m, flush=True))
    teste = post.get("teste", False)

    # 1. decifra o video e publica temporariamente no repositorio
    tmp = f"tmp/{pid}.mp4"
    os.makedirs("tmp", exist_ok=True)
    subprocess.run(["openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2", "-pass", "env:META_TOKEN",
                    "-in", f"{pasta}/video.mp4.enc", "-out", tmp], check=True)
    git("add", tmp); git("commit", "-qm", f"tmp {pid}"); git("push", "-q")
    url = f"https://raw.githubusercontent.com/{REPO}/main/{tmp}"
    time.sleep(10)
    log(f"video temporario: {url}")

    try:
        # 2. Instagram (conta principal + colaboradores)
        if post.get("instagram", True):
            p = dict(media_type="REELS", video_url=url, caption=post["legenda"],
                     share_to_feed="true")
            if post.get("colaboradores"):
                p["collaborators"] = json.dumps(post["colaboradores"])
            c = api("POST", f"{IG['cristoemnoscelioleme']}/media", **p)
            log(f"container IG: {c}")
            cid = c.get("id")
            estado = None
            for _ in range(60):
                time.sleep(10)
                estado = api("GET", cid, fields="status_code,status")
                if estado.get("status_code") in ("FINISHED", "ERROR"):
                    break
            log(f"processamento IG: {estado}")
            if estado.get("status_code") == "FINISHED":
                if teste:
                    log("TESTE: IG pronto, nao publicado")
                else:
                    pub = api("POST", f"{IG['cristoemnoscelioleme']}/media_publish", creation_id=cid)
                    log(f"publicado IG: {pub}")
                    mid = pub.get("id")
                    if mid:
                        perm = api("GET", mid, fields="permalink")
                        st["permalink_ig"] = perm.get("permalink")
                        # 3. aceita convites de colaboracao
                        for nome in post.get("colaboradores", []):
                            ok = False
                            for _ in range(18):
                                time.sleep(10)
                                inv = api("GET", f"{IG[nome]}/collaboration_invites")
                                if any(i.get("media_id") == mid for i in inv.get("data", [])):
                                    r = api("POST", f"{IG[nome]}/collaboration_invites",
                                            media_id=mid, accept="true")
                                    log(f"convite aceito em {nome}: {r}")
                                    ok = True
                                    break
                            if not ok:
                                log(f"convite NAO encontrado em {nome}")
        # 4. Pagina do Facebook
        if post.get("facebook", True):
            pt = api("GET", PAGE, fields="access_token")["access_token"]
            s = api("POST", f"{PAGE}/video_reels", upload_phase="start", token=pt)
            vid = s.get("video_id")
            req = urllib.request.Request(s["upload_url"], method="POST",
                                         headers={"Authorization": f"OAuth {pt}", "file_url": url})
            with urllib.request.urlopen(req, timeout=300) as r:
                log(f"upload FB: {r.read().decode()}")
            f = api("POST", f"{PAGE}/video_reels", upload_phase="finish", video_id=vid,
                    video_state="DRAFT" if teste else "PUBLISHED",
                    description=post["legenda"], token=pt)
            log(f"FB ({'rascunho' if teste else 'publicado'}): {f}")
        # 5. Stories com o trecho inicial do Reel
        if partes_story(pasta) and post.get("story", True):
            pares = [tmp_publico(pid, os.path.basename(f), "mp4") for f in partes_story(pasta)]
            git("add", *[t for t, _ in pares]); git("commit", "-qm", f"tmp story {pid}"); git("push", "-q")
            time.sleep(10)
            try:
                stories_video([u for _, u in pares], post.get("stories_em", ["cristoemnoscelioleme", "celioleme"]),
                              post.get("facebook", True), log, teste)
            finally:
                git("rm", "-q", *[t for t, _ in pares]); git("commit", "-qm", f"remove tmp story {pid}"); git("push", "-q")
    finally:
        # 6. retira o video temporario
        git("rm", "-q", tmp); git("commit", "-qm", f"remove tmp {pid}"); git("push", "-q")
        log("video temporario removido")

    st["fim"] = datetime.datetime.utcnow().isoformat() + "Z"
    salvar_status(pid, st)
    os.rename(f"{pasta}/post.json", f"{pasta}/post.feito.json")
    git("add", "-A", "status", pasta); git("commit", "-qm", f"status {pid}"); git("push", "-q")

def main():
    agora = datetime.datetime.utcnow()
    for pj in sorted(glob.glob("fila/*/post.json")):
        post = json.load(open(pj))
        quando = datetime.datetime.fromisoformat(post["publicar_em_utc"].replace("Z", ""))
        if quando <= agora:
            desde = post.get("somente_se_vazio_desde_utc")
            if desde:  # reserva: so publica se a conta nao publicou nada desde 'desde'
                conta = IG[post.get("conta_reserva", "cristoemnoscelioleme")]
                midias = api("GET", f"{conta}/media", fields="timestamp,media_type", limit=5).get("data", [])
                lim = datetime.datetime.fromisoformat(desde.replace("Z", ""))
                ja = [m for m in midias if datetime.datetime.strptime(m["timestamp"][:19], "%Y-%m-%dT%H:%M:%S") >= lim]
                if ja:
                    print(f"reserva {pj} pulada: conta ja publicou {ja[0]}", flush=True)
                    os.rename(pj, pj.replace("post.json", "post.pulado.json"))
                    git("add", "-A", os.path.dirname(pj)); git("commit", "-qm", f"reserva pulada {pj}"); git("push", "-q")
                    continue
            try:
                publicar(os.path.dirname(pj))
            except Exception as e:
                print(f"ERRO em {pj}: {e}", flush=True)
                if os.path.exists(pj):  # nao tenta de novo sozinho, para nao duplicar post
                    os.rename(pj, pj.replace("post.json", "post.erro.json"))
                    git("add", "-A", os.path.dirname(pj)); git("commit", "-qm", f"erro {pj}"); git("push", "-q")

if __name__ == "__main__":
    main()
