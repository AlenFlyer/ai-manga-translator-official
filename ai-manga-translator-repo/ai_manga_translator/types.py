"""Data models and enums for AI Manga Translator SDK."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Dict, Any

class TaskStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class TargetLanguage(str, Enum):
    ENGLISH = "en"
    JAPANESE = "ja"
    KOREAN = "ko"
    CHINESE = "zh"

@dataclass
class TranslationResult:
    task_id: str
    status: TaskStatus
    target_lang: str
    source_url: Optional[str] = None
    translated_url: Optional[str] = None
    error_message: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None
