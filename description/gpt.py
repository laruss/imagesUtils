from typing import Optional, Literal

from core.ProcessedItem import ProcessedItem
from core.utils import get_logger
from description import settings
from description.prompts import Prompts

logger = get_logger()


def use_gpt(prompt: str, model: Literal['gpt-4', 'gpt-3.5-turbo'] = 'gpt-3.5-turbo') -> Optional[str]:
    import openai

    openai.api_key = settings.openai.api_key

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        choice = response.choices[0]
        assert choice["finish_reason"] == "stop", f"Chat finished unexpectedly: {choice}"

        return choice["message"]["content"]

    except Exception as e:
        logger.warning(f"Failed to use gpt, {e}")


def use_gpt4free(prompt: str, model: Literal['gpt-4', 'gpt-3.5-turbo'] = 'gpt-3.5-turbo') -> Optional[str]:
    import g4f

    try:
        response = g4f.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}])

        return response
    except Exception as e:
        logger.warning(f"Failed to use gpt4free, {e}")


def gpt(
        item: ProcessedItem,
        prompt: Prompts,
        model: Literal['gpt-4', 'gpt-3.5-turbo'] = 'gpt-3.5-turbo',
        used_gpt: Literal['gpt4free', 'openai'] = 'gpt4free'
) -> Optional[str]:
    prompt_text = prompt.value.format(item=item)

    gpt_map = {
        'gpt4free': use_gpt4free,
        'openai': use_gpt
    }

    logger.info(f"Using {used_gpt} to process {item.id}, selected prompt is {prompt.name}.")

    resp_text = gpt_map[used_gpt](prompt_text, model)

    logger.info(f"Processed {item.id} by {used_gpt}, response is {resp_text}")

    return resp_text
