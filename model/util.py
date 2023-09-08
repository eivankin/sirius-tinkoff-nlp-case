import re

SPEAKERS_SWITCH_TOKENS = ("@@ПЕРВЫЙ@@", "@@ВТОРОЙ@@")

def messages_to_prompt(messages: list[str]) -> str:
    """
    Объединяет сообщения из истории в единый контекст, вставляя между ними специальные токены
    :param messages: последние сообщения (не более 3)
    :return: промпт для модели
    """
    return "".join([SPEAKERS_SWITCH_TOKENS[i % 2] + s for i, s in enumerate(messages)])


def model_response_to_message(model_response: str) -> str:
    """
    Достаёт из ответа модели последнюю реплику
    :param model_response: ответ модели
    :return: сообщение для отправки через бот
    """
    return re.split(r'@@[А-Я]+@@', model_response)[-1]