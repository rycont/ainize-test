import streamlit as lit
import torch
from transformers import BartForConditionalGeneration, PreTrainedTokenizerFast

@lit.cache(allow_output_mutation = True)
def loadModels():
  repository = "rycont/biblify"
  _model = BartForConditionalGeneration.from_pretrained(repository)
  _tokenizer = PreTrainedTokenizerFast.from_pretrained(repository)
  
  print("Loaded :)")
  
  return _model, _tokenizer

model, tokenizer = loadModels()

lit.title("성경말투 생성기")
lit.caption("적당한 길이의 한 문장을 넣었을 때 가장 좋은 결과가 나옵니다.")
lit.caption("https://github.com/rycont/kobart-biblify")

text_input = lit.text_area("문장 입력")

MAX_LENGTH = 128

def biblifyWithBeams(beam, tokens, attention_mask):
  generated = model.generate(
    input_ids = torch.Tensor([ tokens ]).to(torch.int64),
    attention_mask = torch.Tensor([ attentionMasks ]).to(torch.int64),
    num_beams = beam,
    max_length = MAX_LENGTH,
    eos_token_id=tokenizer.eos_token_id,
    bad_words_ids=[[tokenizer.unk_token_id]]
   )[0]
   
  return tokenizer.decode(
    generated,
  ).replace('<s>', '').replace('</s>', '')

if len(text_input.strip()) > 0:
  print(text_input)
  
  text_input = "<s>" + text_input + "</s>"
  tokens = tokenizer.encode(text_input)
  
  tokenLength = len(tokens)
  attentionMasks = [ 1 ] * tokenLength + [ 0 ] * (MAX_LENGTH - tokenLength)
  tokens = tokens + [ tokenizer.pad_token_id ] * (MAX_LENGTH - tokenLength)
  
  results = []
  
  for i in range(10)[5:]:
    generated = biblifyWithBeams(
      i + 1,
      tokens,
      attentionMasks
    )
    
    if generated in results:
      print("중복됨")
      continue
      
    results.append(generated)
    with lit.expander(str(len(results)) + "번째 결과 (" + str(i +1) + ")", True):
      lit.write(generated)
      lit.caption(
        "및 " + str(5 - len(results)) + " 개의 중복된 결과")


