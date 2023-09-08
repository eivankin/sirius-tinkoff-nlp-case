from pinferencia import Server
from transformers import AutoTokenizer, AutoModelWithLMHead

import config
import util


model = AutoModelWithLMHead.from_pretrained(config.MODEL_NAME)
tokenizer = AutoTokenizer.from_pretrained("tinkoff-ai/ruDialoGPT-medium")


def predict(messages: list[str]) -> str:
    """
    :param messages: контекст
    :return: ответ модели
    """
    prompt = util.messages_to_prompt(messages)
    inputs = tokenizer(prompt, return_tensors="pt")
    generated_token_ids = model.generate(
        **inputs,
        top_k=10,
        top_p=0.95,
        num_beams=3,
        num_return_sequences=1,
        do_sample=True,
        no_repeat_ngram_size=2,
        temperature=1.2,
        repetition_penalty=1.2,
        length_penalty=1.0,
        eos_token_id=50257 if prompt.endswith(util.SPEAKERS_SWITCH_TOKENS[1]) else 50256,
        max_new_tokens=100
    )
    context_with_response = [
        tokenizer.decode(sample_token_ids) for sample_token_ids in generated_token_ids
    ]
    return util.model_response_to_message(context_with_response[0])


service = Server()
service.register(config.MODEL_NAME, predict)
