# 08 - Títulos

## Objetivo

Gerar sugestões de títulos para shorts e vídeos longos com um score inicial de potencial de clique.

## Onde Acontece

Arquivos principais:

```text
main.py
src/titles/title_generator.py
src/titles/title_rules.py
src/titles/title_schema.py
```

## Entradas

```text
cache/edit_plans/edit_plan.json
cache/context/context.json
cache/emotions/emotions.json
```

Contexto e emoções são carregados, mas hoje ainda são pouco usados na regra final.

## Saída

```text
cache/titles/titles.json
```

Formato:

```json
{
  "suggestions": [
    {
      "target_id": "short_01",
      "target_type": "short",
      "title": "EU NÃO ACREDITO QUE ISSO ACONTECEU",
      "score": 0.8,
      "reason": "gerado a partir do estilo intense"
    }
  ]
}
```

## Como Atua Hoje

1. Carrega o plano de edição.
2. Para cada short, gera variações com base no estilo:
   - `funny`;
   - `intense`;
   - `highlight`.
3. Para cada vídeo longo, gera títulos fixos.
4. Calcula score de cada título.
5. Ordena por score decrescente.
6. Salva `titles.json`.

## Score Atual

O score considera:

- tamanho entre `25` e `60` caracteres;
- palavras fortes como `INSANO`, `ABSURDO`, `ÉPICO`;
- exclamação;
- frases como `NÃO ACREDITO`, `AO VIVO`, `MELHOR`;
- bônus específico para `"EU NÃO ACREDITO QUE ISSO ACONTECEU"`.

## Cache

Usa cache. Se `cache/titles/titles.json` já existe e `force=False`, a etapa é pulada.

## Tempo Observado

Na execução limpa:

```text
Sugestões geradas: 18
Tempo aproximado: < 1s
```

## Gargalos

Baixo impacto.

## Pontos De Otimização

Prioridade baixa para performance, média para qualidade.

Melhorias futuras:

- Usar contexto e emoção para gerar títulos mais específicos.
- Gerar descrições junto com títulos.
- Evitar títulos repetitivos.
- Criar score por plataforma.
- Escolher automaticamente o melhor título por vídeo.
