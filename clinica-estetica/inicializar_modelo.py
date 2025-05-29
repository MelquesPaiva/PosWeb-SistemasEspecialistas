from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

MODELO = "pierreguillou/byt5-small-qa-squad-v1.1-portuguese"
# MODELO = "pierreguillou/t5-base-qa-squad-v1.1-portuguese"

tokenizador = AutoTokenizer.from_pretrained(MODELO)
modelo = AutoModelForSeq2SeqLM.from_pretrained(MODELO)

pipeline("text2text-generation", model=modelo, tokenizer=tokenizador)
