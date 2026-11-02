# cen-publicacao

Publicação automática do Cristo em Nós (Instagram + Página do Facebook).

- `fila/<id>/post.json`: o que publicar e quando (`publicar_em_utc`), legenda, colaboradores.
- `fila/<id>/video.mp4.enc`: vídeo criptografado (só é decifrado na hora de publicar e removido em seguida).
- `status/<id>.json`: resultado de cada publicação.
- Segredo necessário em Settings › Secrets and variables › Actions: `META_TOKEN`.
