# Estado de trabalho (para retomar se o container for trocado)
Atualizado 23/11/2026.
- Container trocado em 23/11: perderam-se /root/.cen (META_TOKEN de cifra e page token) e os scripts de montagem (build.py/rlib.py). Itens já cifrados na fila continuam publicáveis (o GitHub tem o segredo).
- Legendas dos reels: ferramentas/reel/cap.py recria o estilo (Montserrat 800 73px, Cinzel 600 44/40px, tracking 0,14em, dourado 232,196,106). Fontes: github.com/google/fonts (ofl/montserrat, ofl/cinzel).
- Porta aberta v5 (23/11 noite): splice5.py — B03d (Bíblia do ponto de vista do leitor), B04c (igreja pequena entre arranha-céus), B04d (grupo em oração, substitui loft até 33,1 s com fusão para v3). Aguarda aprovação do Celio.
- Gemini: cota semanal ~38 vídeos (reseta sáb 21:56); janela reseta em x:56 variável. Tarefa trig_01CSwHvo7xt52pERppLZK9zU (hora em hora :07) só ENVIA; download/conferência manual (viewport 1280x900 obrigatório).
- Regras de imagem: nada rústico/antigo/"pobrinho"; sem velas, árvores, plantas, ternos, rosto em close; épico moderno elegante.
- Porta aberta v6 (24/11 madrugada): mesmo vídeo da v5; áudio com 28 estalos de "p/b" no microfone removidos (corte <200 Hz por 75 ms em cada estalo, detectados no áudio de voz original). Gravada em REELS\REEL 12 em 24/11. file_uuid fad56cc3-03a2-4a2c-b71f-b58d610d9b62.
- Lição: gravações do Celio têm estalos de microfone nas consoantes "p/b" (soam como batida na mesa). Aplicar a remoção de estalos em todo reel novo antes de entregar.
- 24/11: cifragem — o workflow agora cifra no próprio GitHub Actions qualquer mídia nova enviada sem cifra (feed.jpg, story.jpg, capa.jpg, video.mp4, story*.mp4) antes de publicar. Itens novos podem ir para fila/ em arquivo comum. Recomendação aplicada (opção 1), Celio havia delegado escolhas técnicas.
- Porta aberta v8 (24/11): B04g (igreja de vidro sem cruz; Celio vetou cruz: 'muito batista') no lugar de B04e. splice8.py. Aguarda aprovação.
- Porta aberta v9 (24/11): B04i (salão simples em rua comum, sem cruz) + B05e (mesmo salão por dentro, grupo em círculo). Pedido do Celio: casinha em rua normal, duas cenas no mesmo lugar. splice9.py. B05f ainda na fila como alternativa.
- Porta aberta v10 (25/11 madrugada): B03e (Bíblia lida em casa, abajur, cidade à noite) + B04i + B05f (círculo de oração, sem vaso, rostos baixos). splice10.py. Aguarda aprovação.
- Meus tempos v1 (25/11): build_mt.py (gerador completo: cenas com deslocamento, xfade 0,5, legendas por palavra via faster-whisper com áudio em numpy, cartão final, trilha 0,30 com sidechain, silêncio antes da fala, remoção de estalos). Falta gravar no OneDrive (notebook suspenso) e aprovação.
- 25-26/11: story de 25/11 saiu com título diferente do feed ('atravesso o fogo' x 'atravesso as águas'). Celio apagou; story novo (passarela de vidro sobre águas revoltas, ChatGPT) publicado só-story pelo item fila/2026-11-25-story-aguas-correcao (tipo imagem sem feed.jpg funciona) + manual no FB pessoal. REGRA: antes de enfileirar, conferir que o título do story é idêntico ao do feed. Revisão feita em 26/11: 45 itens da fila até 10/01 conferidos (feed x story, imagem decifrada da própria fila via workflow verificar.yml + chave em /home/claude/keys) — todos os títulos batem. Divergência fila x PRONTOS só em 2027-01-04 ALEGRIA DA SALVAÇÃO (fila: chafariz + fogos; PRONTOS: cachoeira + golfinhos) — Celio achou as duas feias (26/11); nova arte feita (batismo no mar ao nascer do sol, ChatGPT + texto em /home/claude/work/alegria/compor.py), trocada na fila e no PRONTOS; anteriores em PRONTOS\VERSÕES. Aprovada pelo Celio em 26/11 08:01. Para reconferir: editar verificar/pedido.txt e decifrar verificar/sel.cms (apagar do repo depois).
- Cuidado: conferir.py republica story faltante entre 01:20Z e 03:00Z a partir do story.jpg.enc do item do dia; para trocar story, renomear o antigo.
- 26/11: story de 25/11 trocado de novo a pedido do Celio: imagem do feed estendida para 9:16 com Adobe generative expand (fila/2026-11-26-story-aguas-feed). Preferência: quando o story precisar ser refeito às pressas, ele aceita a imagem do feed estendida.

- 26/11: Meus tempos v4 = v3 com T08h (José ~30 anos, caçula, irmãos mais velhos chorando) no lugar de T08e. Gravada em REELS\REEL 13 - MEUS TEMPOS e cena em CENAS. Aprovada 26/11 11:00. Na fila fila/reel13-meus-tempos (05/12 01:00Z = 04/12 22h); capa e legenda aprovadas 26/11 11:44 (CTA ajustado pelo Celio). _PUBLICACAO.txt atualizado (incluída também a linha do REEL 12, que faltava).

- 26/11: áudio de Neemias (REEL 6 PROPÓSITO) recuperado da montagem REEL6_PROPOSITO_v1.mp4 (13/11) separando voz/trilha com demucs -> REELS\REEL 6 - PROPÓSITO\AUDIO_NEEMIAS_RECUPERADO.m4a (109 s, texto completo conferido por transcrição). Gravações do ASR do Celio foram perdidas. Roteiro no doc ROTEIROS MAGOS, NATAL E ANO NOVO (lá datado 08/01). Próximo: aguardar o Celio ouvir; depois cenas novas no padrão atual.

## CALENDÁRIO DE REELS (definido por Claude, Celio delegou as datas em 26/11 18:54)
- 01/12 ter: REEL 12 Porta aberta (na fila)
- 04/12 sex: REEL 13 Meus tempos (na fila)
- 08/12 ter: REEL 14 Resisto ao diabo — v2 entregue 27/11 16:45 (R01c, R02c, R08b, R08c no lugar de R01, R02b, R08), aguarda aprovação
- 11/12 sex: REEL 6 Propósito (Neemias) — áudio recuperado; cenas P01–P12 na fila do Gemini
- 15/12 ter: REEL 15 Sou testemunha (S01–S10; S02/S04/S10 refazer)
- 18/12 sex: livre (sem reel)
- 22/12 ter: REEL 22 Deus cumpre (Simeão)
- 25/12 sex: REEL 7 Deus veio (Natal)
- 29/12 ter: REEL 29 Deus restitui
- 01/01 sex: REEL 8 Nunca passei por aqui (Ano Novo)
- 06/01 qua: REEL 9 Um novo caminho (Magos, Epifania)
- 08/01 sex: REEL 08-01 Sou instrumento de Deus (Ananias)

- 28/11: Resisto: Celio regravou 2 frases (13:04) -> "Ele saiu agora do Jordão cheio do Espírito Santo e foi levado pelo Espírito ao deserto." e "Quarenta dias em jejum, com fome, sozinho." Emendadas em voz.m4a (original em voz_original.m4a); timeline +1,59 s a partir de 43,10 s; legendas e SEG ajustados; words.json refeito. v3 sai com R08d + áudio novo.
- 28/11 13:28: Celio aprovou o áudio emendado v2 (trecho novo com DeepFilterNet + EQ casando com o original). voz.m4a = esse; anteriores em voz_original.m4a e voz_emenda1.m4a.
- 28/11: Escatologia 1 gravado (13:42). 6 erros cortados (olhos/ossos, Isaías, "Em maio", tanques, Efésios 2:4, "não viva distraído") -> AUDIO_ESC01_ISRAEL_EDITADO (3:16). Para caber em 3:00 com o cartão final (limite de recomendação do Instagram): pausas encurtadas + atempo 1,09 -> AUDIO_ESC01_ISRAEL_FINAL (2:55). Pasta REELS\ESCATOLOGIA 01 - ISRAEL O RELÓGIO DE DEUS. Celio trocou o fecho de 1948 para "Deus deu a Israel vitória." Roteiros v5 na pasta REELS.
- 28/11 14:33: Celio aprovou o áudio do Escatologia 1 ("o conjunto está perfeito"), pedindo só tirar o "Em Zacarias 13:8" repetido. Feito: AUDIO_ESC01_ISRAEL_FINAL = 2:53 (aprovado). Próximo: cenas e montagem para 05/01.

## REGRA (Celio, 28/11): a versão PUBLICADA de todo reel fica sempre gravada em OneDrive\CELIO\CHURCH\CRISTO EM NÓS\VIDEOS. Na manhã seguinte à publicação: copiar, marcar "feita" no REELS\_PUBLICACAO.txt e conferir. Arquivo >25 MB: stage → SendUserFile (attach) → device_commit_files com fileUuid. 28/11: REEL 10 e REEL 11 copiados (estavam faltando); linha do REEL 12 incluída no _PUBLICACAO.txt. Lembretes criados para 02/12 e 05/12.
