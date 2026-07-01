"""
manager.py - Φ-Chain Secure Configuration Manager
"""

import os
import logging
from enum import Enum
from typing import Any, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


class Environment(Enum):
    DEV     = "development"
    TESTNET = "testnet"
    MAINNET = "mainnet"


@dataclass
class PhiConfig:
    # ── Φ Constants ─────────────────────────────────────────
    PHI:            float = 1.618033988749895   # Golden Ratio
    PHI_INV:        float = 0.618033988749895   # 1/φ
    PHI_SQUARED:    float = 2.618033988749895   # φ²

    # ── Network ──────────────────────────────────────────────
    ENVIRONMENT:    Environment = Environment.DEV
    NETWORK_NAME:   str = "Φ-Chain Mainnet-Alpha"
    SLOT_DURATION:  int = 8            # F_6 (Fibonacci index 6)
    CHAIN_ID:       int = 1618         # φ-derived
    P2P_PORT:       int = 30303
    API_PORT:       int = 8000
    API_HOST:       str = "127.0.0.1"  # localhost by default — pas 0.0.0.0

    # ── Paths ────────────────────────────────────────────────
    DATA_DIR:       str = "data"
    LOG_DIR:        str = "data/logs"
    REPORT_DIR:     str = "data/reports"

    # ── API Keys (lazy — لا تُقرأ وقت تعريف الـ class) ───────
    OPENAI_API_KEY: Optional[str] = field(
        default=None,
        repr=False   # ← لا تظهر في __repr__ أبداً
    )
    GITHUB_TOKEN:   Optional[str] = field(
        default=None,
        repr=False
    )

    def __post_init__(self):
        # قراءة متأخرة من environment
        if self.OPENAI_API_KEY is None:
            self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        if self.GITHUB_TOKEN is None:
            self.GITHUB_TOKEN = os.getenv("GH_TOKEN")

        # بدّل network name حسب البيئة
        if self.ENVIRONMENT == Environment.TESTNET:
            self.NETWORK_NAME = "Φ-Chain Testnet"
            self.CHAIN_ID = 16180
        elif self.ENVIRONMENT == Environment.DEV:
            self.NETWORK_NAME = "Φ-Chain Dev"
            self.CHAIN_ID = 9999


class ConfigManager:
    _instance: Optional["ConfigManager"] = None  # Singleton

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        env_str = os.getenv("PHI_ENV", "development")
        env     = Environment(env_str)
        self.config = PhiConfig(ENVIRONMENT=env)
        self._initialized = True

    def init_directories(self) -> None:
        """اصرح على هاد الـ method بشكل صريح — لا تشغلها تلقائياً."""
        dirs = [self.config.DATA_DIR, self.config.LOG_DIR, self.config.REPORT_DIR]
        for d in dirs:
            os.makedirs(d, exist_ok=True)
            logger.debug("Directory ensured: %s", d)

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self.config, key, default)

    def is_ai_enabled(self) -> bool:
        key = self.config.OPENAI_API_KEY
        return (
            key is not None
            and key.startswith("sk-")  # minimal format check
            and len(key) > 20
        )

    def is_mainnet(self) -> bool:
        return self.config.ENVIRONMENT == Environment.MAINNET

    def summary(self) -> str:
        """Safe summary — بدون أي secrets."""
        return (
            f"[Φ-Chain Config]\n"
            f"  Network : {self.config.NETWORK_NAME}\n"
            f"  Env     : {self.config.ENVIRONMENT.value}\n"
            f"  Chain ID: {self.config.CHAIN_ID}\n"
            f"  φ       : {self.config.PHI}\n"
            f"  AI      : {'✓' if self.is_ai_enabled() else '✗'}\n"
            f"  GitHub  : {'✓' if self.config.GITHUB_TOKEN else '✗'}"
        )


# لا global instantiation هنا — استعملو بشكل صريح
def get_config() -> ConfigManager:
    return ConfigManager()


if __name__ == "__main__":
    cfg = get_config()
    cfg.init_directories()
    print(cfg.summary())