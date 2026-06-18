# 13 - Plano De Publicação

## Objetivo

Criar uma camada segura de metadados para publicação, sem enviar nada para plataformas externas.

## Onde Acontece

Arquivos principais:

```text
main.py
src/publishing/publish_planner.py
src/publishing/publish_schema.py
src/publishing/youtube_publisher.py
src/publishing/tiktok_publisher.py
src/publishing/instagram_publisher.py
src/publishing/scheduler.py
```

## Entradas

```text
output/shorts/*.mp4
output/long/*.mp4
```

## Saída

```text
cache/publishing/publish_plan.json
```

Formato:

```json
{
  "items": [
    {
      "platform": "youtube_shorts",
      "video_path": "output/shorts/short_01.mp4",
      "title": "SHORT 01",
      "description": "Short gerado automaticamente pelo Video AI Editor.",
      "tags": ["shorts", "live", "gameplay"],
      "scheduled_at": null,
      "privacy_status": "private",
      "status": "pending"
    }
  ]
}
```

## Como Atua Hoje

1. Define a saída em `cache/publishing/publish_plan.json`.
2. Se o plano já existe e `force=False`, reaproveita o cache.
3. Lista todos os MP4 em `output/shorts/`.
4. Para cada short, cria um item com:
   - plataforma `youtube_shorts`;
   - caminho do vídeo;
   - título baseado no nome do arquivo;
   - descrição padrão;
   - tags padrão;
   - privacidade `private`;
   - status `pending`.
5. Lista todos os MP4 em `output/long/`.
6. Para cada vídeo longo, cria um item com:
   - plataforma `youtube`;
   - título padrão;
   - descrição padrão;
   - tags padrão;
   - privacidade `private`;
   - status `pending`.
7. Salva o plano.

## Publicadores

Os arquivos de publicação real ainda são placeholders:

```text
youtube_publisher.py
tiktok_publisher.py
instagram_publisher.py
scheduler.py
```

Eles retornam `not_implemented`. Isso evita upload acidental antes de configurar OAuth, permissões e revisão de app.

## Cache

Usa cache. Se `cache/publishing/publish_plan.json` já existe e `force=False`, a etapa é pulada.

## Tempo Observado

Na execução limpa:

```text
Itens gerados: 6
Tempo aproximado: < 1s
```

## Gargalos

Baixo impacto.

## Pontos De Otimização

Prioridade baixa para performance, média para produto.

Melhorias futuras:

- Usar melhores títulos de `cache/titles/titles.json`.
- Gerar descrições específicas por short.
- Adicionar plataforma TikTok e Instagram ao plano.
- Adicionar agendamento real.
- Implementar upload real com APIs oficiais.
- Registrar status pós-publicação.
