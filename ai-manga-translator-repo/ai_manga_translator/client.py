"""HTTP client implementation for AI Manga Translator API."""

import os
import time
from typing import Optional, Dict, Any, Union
import requests

from .types import TranslationResult, TaskStatus

class MangaTranslatorClient:
    """Client for interacting with the AI Manga Translator service."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://aimangatranslation.com/api",
        timeout: int = 60,
    ):
        self.api_key = api_key or os.getenv("MANGA_TRANSLATOR_API_KEY", "")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})

    def translate_image(
        self,
        image_path: str,
        target_lang: str = "en",
        source_lang: str = "auto",
        style: str = "standard",
    ) -> TranslationResult:
        """Translate a single manga image (JPG, PNG, WebP)."""
        if not os.path.isfile(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        url = f"{self.base_url}/translate"
        data = {
            "target_lang": target_lang,
            "source_lang": source_lang,
            "style": style,
        }

        with open(image_path, "rb") as f:
            files = {"file": f}
            response = self.session.post(url, data=data, files=files, timeout=self.timeout)

        if response.status_code != 200:
            return TranslationResult(
                task_id="",
                status=TaskStatus.FAILED,
                target_lang=target_lang,
                error_message=f"HTTP {response.status_code}: {response.text}",
            )

        res_json = response.json()
        return TranslationResult(
            task_id=res_json.get("task_id", ""),
            status=TaskStatus(res_json.get("status", "completed")),
            target_lang=target_lang,
            translated_url=res_json.get("translated_url"),
            raw_response=res_json,
        )

    def get_task_status(self, task_id: str) -> TranslationResult:
        """Query the status of an ongoing translation job."""
        url = f"{self.base_url}/tasks/{task_id}"
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        res_json = response.json()

        return TranslationResult(
            task_id=task_id,
            status=TaskStatus(res_json.get("status", "pending")),
            target_lang=res_json.get("target_lang", "en"),
            translated_url=res_json.get("translated_url"),
            raw_response=res_json,
        )
