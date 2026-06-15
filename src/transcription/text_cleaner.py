import re

REPLACEMENTS = {
    " neh ": " né ",
    " ta ": " tá ",
    " voce ": " você ",
    " nao ": " não ",
    " mano mano": "mano",
}

def clean_transcript_text(text: str) -> str:
  text = text.strip()
  
  text = re.sub(r"\s+", " ", text)
  
  for wrong, right in REPLACEMENTS.items():
    text = text.replace(wrong, right)
    
  return text