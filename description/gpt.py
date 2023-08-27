from enum import Enum
from typing import Optional

from core.ProcessedItem import ProcessedItem
from core.utils import get_logger
from description.prompt_schema import GPTResponseJSON
from description.settings import GPTSettings

logger = get_logger()


def use_gpt(prompt: str, settings: GPTSettings = GPTSettings(), fall_if_failed: bool = False) -> Optional[str]:
    """
    Use openai api to process prompt

    :param prompt: formatted prompt
    :param settings: GPTSettings
    :param fall_if_failed: bool, whether to raise exception if openai was not generated
    :return: response from openai api, str or None
    """
    import openai

    openai.api_key = settings.openai.api_key.get_secret_value()

    try:
        response = openai.ChatCompletion.create(
            model=settings.model.value, messages=[{"role": "user", "content": prompt}]
        )
        choice = response.choices[0]
        assert (
            choice["finish_reason"] == "stop"
        ), f"Chat finished unexpectedly: {choice}"

        return choice["message"]["content"]

    except Exception as e:
        logger.warning(f"Failed to use gpt, {e}")
        if fall_if_failed:
            raise e


def use_gpt4free(prompt: str, settings: GPTSettings = GPTSettings(), fall_if_failed: bool = False) -> Optional[str]:
    """
    Use gpt4free api to process prompt

    :param prompt: formatted prompt
    :param settings: GPTSettings
    :param fall_if_failed: bool, whether to raise exception if gpt4free was not generated
    :return: str or None
    """
    import g4f

    try:
        response = g4f.ChatCompletion.create(
            model=settings.model.value, messages=[{"role": "user", "content": prompt}]
        )

        return response

    except Exception as e:
        logger.warning(f"Failed to use gpt4free, {e}")
        if fall_if_failed:
            raise e


def _get_prompt(item: ProcessedItem, settings: GPTSettings = GPTSettings()) -> str:
    """
    Get prompt for gpt

    :param item: ProcessedItem
    :param settings: GPTSettings
    :return: prompt, str
    """
    prompt = settings.prompt.value.format(item=item)

    if settings.use_prompt_schema:
        prompt = f"{prompt}\nYou need to correspond to the following schema:\n{GPTResponseJSON.model_json_schema()}"

    return prompt


def gpt(item: ProcessedItem, settings: GPTSettings = GPTSettings(), fall_if_failed: bool = False) -> Optional[str]:
    """
    Use gpt to process item
    :param item: ProcessedItem
    :param settings: GPTSettings
    :param fall_if_failed: bool, whether to raise exception if gpt was not generated
    :return: gpt text, str or None
    """
    mapper = {"openai": use_gpt, "gpt4free": use_gpt4free}

    if settings.skip_gpt_if_gpted and item.gptText:
        logger.info(f"Skipping {item.id}, already gpted")

        return item.gptText

    prompt_text = _get_prompt(item, settings)

    service = settings.service.name

    logger.info(
        f"Using {service} to process {item.id}, selected prompt is {settings.prompt.name}."
    )

    resp_text = mapper[service](prompt_text, settings, fall_if_failed)

    if resp_text == "":
        logger.warning(f"Got empty response from {service} for {item.id}, skipping")

        return None

    logger.info(f"Processed {item.id} by {service}, response is {resp_text}")

    return resp_text
