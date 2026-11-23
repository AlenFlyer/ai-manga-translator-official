"""Official Python SDK and CLI for AI Manga Translator."""

from .client import MangaTranslatorClient
from .types import TranslationResult, TaskStatus

__version__ = "0.1.0"
__all__ = ["MangaTranslatorClient", "TranslationResult", "TaskStatus"]
