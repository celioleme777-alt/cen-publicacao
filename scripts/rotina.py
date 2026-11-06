"""Orquestra uma execução: espera itens que vencem em breve (o agendador do GitHub atrasa até ~70 min),
publica, espelha no Facebook e confere. Tudo em UTC."""
import json, glob, os, subprocess, time, datetime as dt
UTC = dt.timezone.utc
def agora(): return dt.datetime.now(UTC)
def rodar(s): subprocess.run(["python3", f"scripts/{s}"], check=False)
def proximo_vencimento(janela_min=75):
    lim = agora() + dt.timedelta(minutes=janela_min); prox = None
    for f in glob.glob("fila/*/post.json"):
        try: p = json.load(open(f))
        except Exception: continue
        t = p.get("publicar_em_utc")
        if not t: continue
        t = dt.datetime.fromisoformat(t.replace("Z", "+00:00"))
        if agora() < t <= lim and (prox is None or t < prox): prox = t
    return prox
def dormir_ate(t):
    s = (t - agora()).total_seconds()
    if s > 0: print(f"aguardando até {t.isoformat()} ({s/60:.1f} min)", flush=True); time.sleep(s)
def noite(h, m): # horário de hoje (UTC) — a janela das 22h BRT cai entre 00:50 e 03:00 UTC
    n = agora(); return n.replace(hour=h, minute=m, second=0, microsecond=0)
# 1) se algo vence nos próximos 75 min, espera e publica na hora
p = proximo_vencimento()
if p: dormir_ate(p + dt.timedelta(seconds=20))
rodar("publicar.py")
# 2) janela das 22h BRT: pega também os itens das 22h10 (story da Página) e espelha os posts do Business Suite
if noite(0, 50) <= agora() <= noite(1, 20):
    dormir_ate(noite(1, 11)); rodar("publicar.py")
    rodar("espelhar.py")
    dormir_ate(noite(1, 21)); rodar("conferir.py")
else:
    rodar("espelhar.py"); rodar("conferir.py")
