# 01 - Extração de Áudio

## Status Atual

- Tempo atual de referência: `36.76s` para vídeo de `57min21s`
- Otimização inicial: concluída
- Prioridade: Média
- Processo base: `documentation/PROCESSOS/01 - EXTRAÇÃO DE ÁUDIO.md`

## Já Feito

- Medição de tempo real.
- Uso de `-map 0:a:0`.
- Validação do WAV extraído.
- Metadata da extração.
- Modo rápido de teste.
- Cache com assinatura do vídeo.
- Chunking do áudio em `cache/audio/chunks/`.

## Resultado Atual

O áudio extraído agora usa assinatura baseada em `file_size + modified_time`.

Exemplo:

```text
cache/audio/live_bruta_a1b2c3d4e5f6.wav
cache/audio/live_bruta_a1b2c3d4e5f6_audio_metadata.json
cache/audio/chunks/live_bruta_a1b2c3d4e5f6/duration_900_overlap_2/
```

Isso evita reutilizar o WAV errado quando um vídeo é trocado mantendo o mesmo nome.

## Melhorias Pendentes

1. Evitar releitura pesada do áudio em etapas seguintes.
   - Prioridade: Alta.
   - Impacto: alto para lives longas.
   - Risco: médio.
   - Ideia: gerar `audio_features.json` com energia, picos e métricas reutilizáveis.

2. Criar áudio separado por finalidade.
   - Prioridade: Média.
   - Impacto: médio.
   - Risco: médio.
   - Exemplo: um arquivo otimizado para transcrição e outro para análise de intensidade.

3. Validar se WAV PCM ainda é o melhor formato intermediário.
   - Prioridade: Média.
   - Impacto: médio.
   - Risco: médio, porque análise de energia atual espera WAV.

## Deixar Para Depois

- Áudio comprimido.
- Formato intermediário diferente de `pcm_s16le`.
- Integração completa entre `cache/audio/chunks/` e features reutilizáveis.
