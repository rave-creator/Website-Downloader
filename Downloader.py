# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║   ████████╗██╗████████╗ █████╗ ███╗   ██╗    ██████╗ ███╗   ███╗ ██████╗       ║
║      ██║   ██║   ██║   ██╔══██╗████╗  ██║   ██╔═══██╗████╗ ████║██╔════╝       ║
║      ██║   ██║   ██║   ███████║██╔██╗ ██║   ██║   ██║██╔████╔██║██║  ███╗      ║
║      ██║   ██║   ██║   ██╔══██║██║╚██╗██║   ██║   ██║██║╚██╔╝██║██║   ██║      ║
║      ██║   ██║   ██║   ██║  ██║██║ ╚████║   ╚██████╔╝██║ ╚═╝ ██║╚██████╔╝      ║
║      ╚═╝   ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝    ╚═════╝ ╚═╝     ╚═╝ ╚═════╝       ║
║                                                                                  ║
║                    ◆ NEXUS CORE v8.0 — 2026 SOVEREIGN EDITION ◆                 ║
║              Ultra-Technical Intelligence & Deep Archival Framework              ║
╚══════════════════════════════════════════════════════════════════════════════════╝

Author   : ARCHITECT_PRIME // TITAN CORE TEAM
Engine   : AsyncIO + aiohttp + Rich TUI v2
Mode     : NEXUS_FULL — Bypass / Stealth / Mirror / OSINT
Build    : 20260101-APEX
"""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# BOOTSTRAP — AUTO DEPENDENCY RESOLVER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

import sys
import subprocess
import os

_REQUIRED = {
    "requests":       "requests>=2.31.0",
    "rich":           "rich>=13.7.0",
    "psutil":         "psutil>=5.9.0",
    "aiohttp":        "aiohttp>=3.9.0",
    "beautifulsoup4": "beautifulsoup4>=4.12.0",
    "lxml":           "lxml>=4.9.0",
    "cryptography":   "cryptography>=41.0.0",
    "fake_useragent": "fake-useragent>=1.4.0",
    "curl_cffi":      "curl-cffi>=0.5.10",
    "tqdm":           "tqdm>=4.66.0",
    "dnspython":      "dnspython>=2.4.0",
    "Wappalyzer":     "python-Wappalyzer>=0.3.1",
}

def _bootstrap():
    missing = []
    for mod, pkg in _REQUIRED.items():
        try:
            __import__(mod.split(".")[0])
        except ImportError:
            missing.append(pkg)
    if missing:
        print(f"\n[TITAN] Installing {len(missing)} packages...", flush=True)
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-q", "--upgrade", "--break-system-packages"] + missing,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        print("[TITAN] Dependencies ready.\n", flush=True)

_bootstrap()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# IMPORTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

import asyncio
import hashlib
import json
import logging
import mimetypes
import random
import re
import shutil
import signal
import socket
import ssl
import threading
import time
import uuid
import datetime
import struct
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from urllib.parse import urljoin, urlparse, urlencode, quote

import aiohttp
import psutil
import requests
from bs4 import BeautifulSoup

from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.columns import Columns
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import (BarColumn, DownloadColumn, MofNCompleteColumn,
                            Progress, SpinnerColumn, TaskProgressColumn,
                            TextColumn, TimeElapsedColumn, TransferSpeedColumn)
from rich.prompt import Confirm, Prompt
from rich.rule import Rule
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.tree import Tree
from rich.traceback import install as _install_tb

_install_tb(show_locals=False, suppress=[aiohttp, requests])

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GLOBAL CONFIG & PATHS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BASE   = Path(__file__).parent
ARCH   = BASE / "NEXUS_ARCHIVES"
LOGS   = BASE / "NEXUS_RESOURCES" / "logs"
TMP    = BASE / "NEXUS_RESOURCES" / "tmp"
CACHE  = BASE / "NEXUS_RESOURCES" / "cache"
REP    = BASE / "NEXUS_REPORTS"
WORDL  = BASE / "NEXUS_RESOURCES" / "wordlists"

for _d in [ARCH, LOGS, TMP, CACHE, REP, WORDL]:
    _d.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s │ %(levelname)-8s │ %(name)s │ %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.FileHandler(LOGS / "nexus.log", encoding="utf-8"),
    ],
)
log = logging.getLogger("NEXUS")

console = Console(highlight=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# USER-AGENT POOL — BYPASS LAYER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

UA_POOL = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/131.0.0.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
]

REFERERS = [
    "https://www.google.com/",
    "https://duckduckgo.com/",
    "https://www.bing.com/",
    "https://search.yahoo.com/",
    "https://www.google.fr/",
]

def get_stealth_headers(extra: dict = None) -> dict:
    """
    Generate convincing browser-like headers.
    IMPORTANT: Accept-Encoding is intentionally set to 'identity' to prevent
    aiohttp content-encoding decode errors (brotli/zstd mismatches from servers).
    Link extraction still works perfectly on raw HTML.
    """
    h = {
        "User-Agent":                random.choice(UA_POOL),
        "Accept":                    "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language":           "en-US,en;q=0.9,fr;q=0.7",
        # 'identity' = no compression → zero ContentEncoding decode errors
        "Accept-Encoding":           "identity",
        "Connection":                "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest":            "document",
        "Sec-Fetch-Mode":            "navigate",
        "Sec-Fetch-Site":            "cross-site",
        "Cache-Control":             "no-cache",
        "Pragma":                    "no-cache",
        "Referer":                   random.choice(REFERERS),
        "DNT":                       "1",
    }
    if extra:
        h.update(extra)
    return h

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# NEXUS BYPASS CORE v3.0 — SOVEREIGN EDITION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# ── Browser fingerprint tables ────────────────────────────────────────────────

# Full UA pool with exact build versions
UA_POOL = [
    # Chrome Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.117 Safari/537.36",
    # Chrome macOS
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36",
    # Chrome Linux
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36",
    # Firefox
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.2; rv:122.0) Gecko/20100101 Firefox/122.0",
    # Safari
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    # Edge
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.2903.86",
    # Mobile Chrome
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
]

# Sec-CH-UA per UA — must match exactly
_CH_UA_MAP = {
    "Chrome/131.0.6778.86": (
        '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "?0", "Windows"
    ),
    "Chrome/130.0.6723.117": (
        '"Google Chrome";v="130", "Chromium";v="130", "Not_A Brand";v="99"',
        "?0", "macOS"
    ),
    "Edg/131.0.2903.86": (
        '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "?0", "Windows"
    ),
}

_ACCEPT_MAP = {
    "Chrome":  "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Firefox": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Safari":  "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Edge":    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Mobile":  "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
}

_ACCEPT_LANG = [
    "en-US,en;q=0.9",
    "en-GB,en;q=0.9,fr;q=0.8",
    "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
    "en-US,en;q=0.9,es;q=0.8,pt;q=0.7",
    "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7",
    "en-CA,en;q=0.9,fr-CA;q=0.8",
]

# Realistic CDN/ISP IPs for X-Forwarded-For
_FORWARD_IP_RANGES = [
    # Major CDN edge nodes
    "185.93.228.{}", "185.93.229.{}", "31.13.92.{}",
    # ISP ranges (France)
    "77.136.{}.{}", "90.63.{}.{}", "82.64.{}.{}",
    # ISP ranges (US)
    "73.{}.{}.{}", "174.{}.{}.{}", "98.{}.{}.{}",
    # ISP ranges (DE)
    "91.{}.{}.{}", "88.{}.{}.{}",
]

def _random_ip() -> str:
    tpl = random.choice(_FORWARD_IP_RANGES)
    parts = tpl.count("{}")
    nums  = [random.randint(1, 254) for _ in range(parts)]
    return tpl.format(*nums)

REFERERS = [
    "https://www.google.com/",
    "https://www.google.fr/",
    "https://duckduckgo.com/",
    "https://www.bing.com/",
    "https://search.yahoo.com/",
    "https://www.google.de/",
    "https://t.co/",
    "https://l.facebook.com/",
    "https://www.reddit.com/",
    "https://news.ycombinator.com/",
]

# ── WAF cookie names to capture & replay ──────────────────────────────────────
WAF_COOKIE_NAMES = [
    "cf_clearance", "__cf_bm", "__cfruid", "__cfwaitingroom",
    "AWSALB", "AWSALBCORS", "AWSALBAPP",
    "incap_ses_", "visid_incap_", "nlbi_",
    "ddg_cookie", "ddos_guard_session", "_ddg",
    "ak_bmsc", "bm_sz", "bm_sv",
    "_abck", "BVBID",
    "sucuri_cloudproxy_uuid_",
    "__utmz", "PHPSESSID",
]

# ── Per-domain AI strategy state ───────────────────────────────────────────────
@dataclass
class DomainState:
    domain: str
    waf_type: Optional[str]           = None
    best_ua: Optional[str]            = None
    best_proxy: Optional[str]         = None
    success_count: int                = 0
    fail_count: int                   = 0
    challenge_count: int              = 0
    last_success_ts: float            = 0.0
    avg_delay: float                  = 0.3
    detected_challenges: List[str]    = field(default_factory=list)
    strategy: str                     = "STEALTH"     # STEALTH → SPOOF → PROXY → ROTATE
    strategy_locked: bool             = False
    cookies: Dict[str, str]           = field(default_factory=dict)
    referer: str                      = ""
    session_ua: Optional[str]         = None          # locked UA for session
    session_ip: Optional[str]         = None          # locked fake-IP for session
    proxy_scores: Dict[str, float]    = field(default_factory=dict)

    @property
    def success_rate(self) -> float:
        total = self.success_count + self.fail_count
        return (self.success_count / total * 100) if total > 0 else 0.0

    @property
    def should_escalate(self) -> bool:
        return self.fail_count >= 3 and not self.strategy_locked

# ── Proxy record ──────────────────────────────────────────────────────────────
@dataclass
class ProxyRecord:
    url: str
    protocol: str                     = "http"
    latency_ms: int                   = 9999
    success: int                      = 0
    failures: int                     = 0
    last_check: float                 = 0.0
    alive: bool                       = True
    blacklisted: bool                 = False
    blacklist_until: float            = 0.0

    @property
    def score(self) -> float:
        if self.blacklisted and time.time() < self.blacklist_until:
            return -1.0
        total = self.success + self.failures
        if total == 0:
            return 50.0
        rate = self.success / total * 100
        lat_penalty = min(self.latency_ms / 100, 50)
        return max(0.0, rate - lat_penalty)

# ── Free proxy source URLs ─────────────────────────────────────────────────────
FREE_PROXY_APIS = [
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=elite",
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=5000&country=all",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
]

class BypassEngine:
    """
    NEXUS Bypass Core v3.0
    Fully autonomous WAF/CDN bypass engine with adaptive AI.

    Strategies (auto-escalated per domain):
      STEALTH  — Browser fingerprint + header spoof + cookie replay
      SPOOF    — Above + aggressive IP forwarding + WAF-specific tricks
      PROXY    — Route through proxy pool with smart rotation
      ROTATE   — Rapid proxy + UA + IP rotation on each attempt
    """

    def __init__(self):
        self._domain_states: Dict[str, DomainState]   = {}
        self._proxy_records: Dict[str, ProxyRecord]    = {}
        self._proxy_list: List[str]                    = []
        self._proxy_lock  = asyncio.Lock() if False else None  # created lazily
        self._req_count   = 0
        self._total_bypassed = 0
        self._total_blocked  = 0
        self._last_proxy_fetch: float = 0.0
        self._auto_proxy_enabled: bool = False
        log.info("[BYPASS] NexusBypass v3.0 initialized")

    # ═══════════════════════════════════════════════════════════════
    # DOMAIN STATE / AI BRAIN
    # ═══════════════════════════════════════════════════════════════

    def _get_state(self, domain: str) -> DomainState:
        if domain not in self._domain_states:
            self._domain_states[domain] = DomainState(domain=domain)
        return self._domain_states[domain]

    def _record_success(self, domain: str, proxy: Optional[str] = None):
        state = self._get_state(domain)
        state.success_count    += 1
        state.last_success_ts   = time.time()
        state.fail_count        = max(0, state.fail_count - 1)  # partial recovery
        self._total_bypassed   += 1
        if proxy:
            rec = self._proxy_records.get(proxy)
            if rec:
                rec.success += 1

    def _record_failure(self, domain: str, reason: str, proxy: Optional[str] = None):
        state = self._get_state(domain)
        state.fail_count += 1
        self._total_blocked += 1
        if proxy:
            rec = self._proxy_records.get(proxy)
            if rec:
                rec.failures += 1
                if rec.failures >= 3:
                    rec.blacklisted     = True
                    rec.blacklist_until = time.time() + 300  # 5min blacklist
                    log.debug(f"[BYPASS] Proxy blacklisted: {proxy}")
        # Escalate strategy
        if state.should_escalate:
            self._escalate_strategy(state, reason)

    def _escalate_strategy(self, state: DomainState, reason: str):
        ladder = ["STEALTH", "SPOOF", "PROXY", "ROTATE"]
        try:
            idx = ladder.index(state.strategy)
            if idx < len(ladder) - 1:
                new_strat = ladder[idx + 1]
                log.warning(f"[AI] {state.domain}: Escalating {state.strategy} → {new_strat} (reason: {reason})")
                state.strategy   = new_strat
                state.fail_count = 0
                # Reset session fingerprint on escalation
                state.session_ua = None
                state.session_ip = None
        except ValueError:
            pass

    def _adapt_delay(self, state: DomainState):
        """AI-adjust delay: if getting challenges, slow down."""
        if state.challenge_count > 2:
            state.avg_delay = min(state.avg_delay * 1.5, 5.0)
        elif state.success_count > 10:
            state.avg_delay = max(state.avg_delay * 0.9, 0.1)

    # ═══════════════════════════════════════════════════════════════
    # PROXY MANAGEMENT
    # ═══════════════════════════════════════════════════════════════

    def load_proxies(self, proxy_list: List[str]):
        added = 0
        for p in proxy_list:
            p = p.strip()
            if not p or p.startswith("#"):
                continue
            # Normalize format
            if not p.startswith(("http://","https://","socks4://","socks5://")):
                p = "http://" + p
            if p not in self._proxy_records:
                proto = p.split("://")[0]
                self._proxy_records[p] = ProxyRecord(url=p, protocol=proto)
                added += 1
        self._proxy_list = list(self._proxy_records.keys())
        log.info(f"[BYPASS] Proxy pool: {len(self._proxy_list)} total (+{added} new)")

    def load_proxies_from_file(self, path: str):
        try:
            lines = Path(path).read_text(encoding="utf-8", errors="ignore").splitlines()
            self.load_proxies(lines)
            console.print(f"[green]✓ Loaded {len(lines)} proxies from {path}[/]")
        except Exception as e:
            log.warning(f"[BYPASS] Proxy file error: {e}")

    async def fetch_free_proxies(self, max_sources: int = 3):
        """Auto-fetch proxies from public lists."""
        console.print("[yellow]⬇  Fetching free proxy lists…[/]")
        all_proxies = []
        sources = random.sample(FREE_PROXY_APIS, min(max_sources, len(FREE_PROXY_APIS)))

        async def _get_source(url):
            try:
                connector = aiohttp.TCPConnector(ssl=False)
                async with aiohttp.ClientSession(connector=connector) as s:
                    async with s.get(url, timeout=aiohttp.ClientTimeout(total=10)) as r:
                        if r.status == 200:
                            text = await r.text(errors="replace")
                            return [line.strip() for line in text.splitlines()
                                    if re.match(r"\d+\.\d+\.\d+\.\d+:\d+", line.strip())]
            except Exception:
                return []
            return []

        results = await asyncio.gather(*[_get_source(u) for u in sources], return_exceptions=True)
        for r in results:
            if isinstance(r, list):
                all_proxies.extend(r)

        self.load_proxies(list(set(all_proxies)))
        console.print(f"[green]✓ Fetched {len(all_proxies)} proxies[/]")
        return len(all_proxies)

    async def health_check_proxies(self, test_url: str = "https://httpbin.org/ip", max_concurrent: int = 50):
        """Test all proxies in parallel, rank by latency."""
        if not self._proxy_list:
            console.print("[yellow]No proxies to check.[/]")
            return
        console.print(f"[yellow]🔍 Health-checking {len(self._proxy_list)} proxies…[/]")
        sem = asyncio.Semaphore(max_concurrent)
        alive = 0

        async def _check(proxy_url: str):
            nonlocal alive
            async with sem:
                rec = self._proxy_records.get(proxy_url)
                if not rec:
                    return
                t0 = time.time()
                try:
                    connector = aiohttp.TCPConnector(ssl=False)
                    async with aiohttp.ClientSession(connector=connector) as s:
                        async with s.get(
                            test_url,
                            proxy=proxy_url,
                            timeout=aiohttp.ClientTimeout(total=8),
                            headers={"User-Agent": random.choice(UA_POOL)},
                        ) as r:
                            if r.status in (200, 301, 302):
                                rec.latency_ms  = int((time.time()-t0)*1000)
                                rec.alive       = True
                                rec.blacklisted = False
                                alive += 1
                            else:
                                rec.alive = False
                except Exception:
                    rec.alive = False
                rec.last_check = time.time()

        await asyncio.gather(*[_check(p) for p in self._proxy_list], return_exceptions=True)
        # Remove dead proxies
        self._proxy_list = [p for p, r in self._proxy_records.items() if r.alive]
        # Sort by score
        self._proxy_list.sort(key=lambda p: self._proxy_records[p].score, reverse=True)
        console.print(f"[green]✓ {alive}/{len(self._proxy_records)} proxies alive[/]")

    def _pick_proxy(self, domain: str = "") -> Optional[str]:
        """Smart proxy selection: prefer high-score proxies, avoid blacklisted."""
        state = self._get_state(domain) if domain else None
        alive = [
            p for p in self._proxy_list
            if p in self._proxy_records
            and self._proxy_records[p].alive
            and not (
                self._proxy_records[p].blacklisted
                and time.time() < self._proxy_records[p].blacklist_until
            )
        ]
        if not alive:
            return None
        # Weighted random: higher score = higher chance
        scores = [max(0.1, self._proxy_records[p].score) for p in alive]
        total  = sum(scores)
        r      = random.uniform(0, total)
        cum    = 0.0
        for p, s in zip(alive, scores):
            cum += s
            if cum >= r:
                return p
        return alive[0] if alive else None

    # ═══════════════════════════════════════════════════════════════
    # BROWSER FINGERPRINT ENGINE
    # ═══════════════════════════════════════════════════════════════

    def _ua_type(self, ua: str) -> str:
        if "Edg/" in ua:              return "Edge"
        if "Firefox/" in ua:          return "Firefox"
        if "Safari/" in ua and "Chrome" not in ua: return "Safari"
        if "Mobile" in ua:            return "Mobile"
        return "Chrome"

    def _get_ch_ua(self, ua: str) -> Optional[Tuple[str, str, str]]:
        for key, val in _CH_UA_MAP.items():
            if key in ua:
                return val
        # Fallback: generate from UA string
        m = re.search(r"Chrome/(\d+)\.", ua)
        if m:
            v = m.group(1)
            return (f'"Google Chrome";v="{v}", "Chromium";v="{v}", "Not_A Brand";v="24"',
                    "?0", "Windows")
        return None

    def build_headers(self, url: str, state: DomainState) -> dict:
        """Construct full browser-matching header set."""
        domain = urlparse(url).netloc

        # Lock UA/IP within a session for consistency
        if not state.session_ua:
            state.session_ua = random.choice(UA_POOL)
        if not state.session_ip:
            state.session_ip = _random_ip()

        ua      = state.session_ua
        ip      = state.session_ip
        btype   = self._ua_type(ua)
        accept  = _ACCEPT_MAP.get(btype, _ACCEPT_MAP["Chrome"])
        referer = state.referer or random.choice(REFERERS)
        lang    = random.choice(_ACCEPT_LANG)

        h = {
            "User-Agent":                ua,
            "Accept":                    accept,
            "Accept-Language":           lang,
            "Accept-Encoding":           "identity",
            "Connection":                "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control":             "no-cache",
            "Pragma":                    "no-cache",
        }

        # Sec-Fetch context
        same_origin = bool(state.referer and domain in state.referer)
        h.update({
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin" if same_origin else "cross-site",
            "Sec-Fetch-User": "?1",
        })

        # Chrome/Edge Client Hints
        if btype in ("Chrome", "Edge"):
            ch = self._get_ch_ua(ua)
            if ch:
                ch_ua, mobile, platform = ch
                h.update({
                    "Sec-CH-UA":                   ch_ua,
                    "Sec-CH-UA-Mobile":            mobile,
                    "Sec-CH-UA-Platform":          f'"{platform}"',
                    "Sec-CH-UA-Platform-Version":  '"15.0.0"',
                    "Sec-CH-UA-Full-Version-List": ch_ua,
                    "Sec-CH-UA-Arch":              '"x86"',
                    "Sec-CH-UA-Bitness":           '"64"',
                    "Sec-CH-UA-WoW64":             "?0",
                })

        # Referer
        if state.referer:
            h["Referer"] = state.referer

        # SPOOF/ROTATE strategies: add IP forwarding headers
        if state.strategy in ("SPOOF", "PROXY", "ROTATE"):
            forward_chain = f"{ip}, {_random_ip()}, 127.0.0.1"
            h.update({
                "X-Forwarded-For":    forward_chain,
                "X-Real-IP":          ip,
                "X-Originating-IP":   ip,
                "X-Remote-IP":        ip,
                "X-Client-IP":        ip,
                "True-Client-IP":     ip,
                "X-Forwarded-Host":   domain,
                "X-Forwarded-Proto":  "https",
                "X-Forwarded-Port":   "443",
                "X-Forwarded-Scheme": "https",
                "X-Host":             domain,
                "X-Custom-IP-Authorization": ip,
            })

        # WAF-specific
        waf = state.waf_type
        if waf == "CLOUDFLARE":
            h.update({
                "CF-Connecting-IP": ip,
                "CF-IPCountry":     random.choice(["FR","US","DE","GB","NL","BE","CA","AU"]),
                "CF-Visitor":       '{"scheme":"https"}',
                "CDN-Loop":         "cloudflare",
            })
        elif waf == "AKAMAI":
            h.update({
                "Akamai-Origin-Hop":               "1",
                "X-Akamai-Device-Characteristics": "is_wireless_device=false",
                "X-Akamai-Config-Log-Detail":      "true",
            })
        elif waf in ("IMPERVA", "INCAPSULA"):
            h.update({
                "X-Forwarded-Host":    domain,
                "X-Original-URL":      urlparse(url).path or "/",
                "X-Rewrite-URL":       urlparse(url).path or "/",
            })
        elif waf == "DDOSGUARD":
            h["X-Forwarded-Server"] = domain
        elif waf == "AWS-SHIELD":
            h["X-Amzn-Trace-Id"] = f"Root=1-{uuid.uuid4().hex[:8]}-{uuid.uuid4().hex[:12]}"

        # Cookie header from stored WAF cookies
        c = state.cookies
        if c:
            h["Cookie"] = "; ".join(f"{k}={v}" for k, v in c.items())

        return h

    # ═══════════════════════════════════════════════════════════════
    # TLS FINGERPRINT ENGINE
    # ═══════════════════════════════════════════════════════════════

    @staticmethod
    def make_tls_context(profile: str = "chrome") -> ssl.SSLContext:
        """
        Build SSLContext mimicking real browser TLS fingerprint.
        Chrome 131: TLS 1.3 preferred, modern AEAD ciphers, ECDH.
        """
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.check_hostname = False
        ctx.verify_mode    = ssl.CERT_NONE

        try:
            ctx.minimum_version = ssl.TLSVersion.TLSv1_2
        except AttributeError:
            pass

        _CHROME_CIPHERS = [
            "TLS_AES_128_GCM_SHA256",
            "TLS_AES_256_GCM_SHA384",
            "TLS_CHACHA20_POLY1305_SHA256",
            "ECDHE-ECDSA-AES128-GCM-SHA256",
            "ECDHE-RSA-AES128-GCM-SHA256",
            "ECDHE-ECDSA-AES256-GCM-SHA384",
            "ECDHE-RSA-AES256-GCM-SHA384",
            "ECDHE-ECDSA-CHACHA20-POLY1305",
            "ECDHE-RSA-CHACHA20-POLY1305",
            "ECDHE-RSA-AES128-SHA256",
            "ECDHE-RSA-AES256-SHA384",
            "ECDHE-RSA-AES128-SHA",
            "ECDHE-RSA-AES256-SHA",
            "AES128-GCM-SHA256",
            "AES256-GCM-SHA384",
            "AES128-SHA256",
            "AES256-SHA256",
        ]
        _FIREFOX_CIPHERS = [
            "TLS_AES_128_GCM_SHA256",
            "TLS_CHACHA20_POLY1305_SHA256",
            "TLS_AES_256_GCM_SHA384",
            "ECDHE-ECDSA-AES128-GCM-SHA256",
            "ECDHE-RSA-AES128-GCM-SHA256",
            "ECDHE-ECDSA-CHACHA20-POLY1305",
            "ECDHE-RSA-CHACHA20-POLY1305",
            "ECDHE-ECDSA-AES256-GCM-SHA384",
            "ECDHE-RSA-AES256-GCM-SHA384",
            "ECDHE-ECDSA-AES256-SHA",
            "ECDHE-ECDSA-AES128-SHA",
            "ECDHE-RSA-AES128-SHA",
            "ECDHE-RSA-AES256-SHA",
            "AES128-GCM-SHA256",
            "AES256-GCM-SHA384",
        ]
        ciphers = _FIREFOX_CIPHERS if profile == "firefox" else _CHROME_CIPHERS
        try:
            ctx.set_ciphers(":".join(ciphers))
        except ssl.SSLError:
            pass  # OpenSSL version fallback

        # Set ALPN (h2, http/1.1 — Chrome order)
        try:
            ctx.set_alpn_protocols(["h2", "http/1.1"])
        except Exception:
            pass

        return ctx

    # ═══════════════════════════════════════════════════════════════
    # CHALLENGE DETECTION
    # ═══════════════════════════════════════════════════════════════

    @staticmethod
    def classify_challenge(status: int, body: bytes, headers: dict) -> Optional[str]:
        """
        Classify WAF challenge/block type from response.
        Returns challenge string or None if clean.
        """
        if not body:
            return None

        preview = body[:8192].decode("utf-8", errors="replace").lower()
        server  = headers.get("Server", "").lower()
        via     = headers.get("Via", "").lower()
        cf_ray  = headers.get("CF-Ray", "")

        # ── Cloudflare ─────────────────────────────────────────────
        if cf_ray or "cloudflare" in server:
            if status == 403:
                if "1003" in preview or "direct ip" in preview:
                    return "CF_DIRECT_IP"
                if "1010" in preview or "browser" in preview:
                    return "CF_BROWSER_CHECK"
                return "CF_403"
            if status == 503:
                if "checking your browser" in preview or "cf-chl" in preview:
                    return "CF_JS_CHALLENGE"
                if "jschl" in preview or "challenge-running" in preview:
                    return "CF_JS_CHALLENGE"
            if status == 429:
                return "CF_RATE_LIMIT"
            if status == 520:
                return "CF_ORIGIN_ERROR"
            if "captcha" in preview or "hcaptcha" in preview:
                return "CF_CAPTCHA"
            if "turnstile" in preview:
                return "CF_TURNSTILE"

        # ── DDoS-Guard ────────────────────────────────────────────
        if "ddos-guard" in preview or "ddos guard" in preview:
            return "DDOSGUARD_CHALLENGE"
        if "ddos" in headers.get("Server","").lower():
            return "DDOSGUARD_CHALLENGE"

        # ── Imperva/Incapsula ─────────────────────────────────────
        if "incapsula" in preview or "imperva" in preview:
            if "captcha" in preview:
                return "IMPERVA_CAPTCHA"
            return "IMPERVA_CHALLENGE"
        if "incap_ses_" in headers.get("Set-Cookie",""):
            if status in (403, 503):
                return "IMPERVA_CHALLENGE"

        # ── Akamai ────────────────────────────────────────────────
        if "akamai" in server or "ak " in via:
            if status in (403, 503):
                return "AKAMAI_BLOCK"

        # ── AWS WAF ───────────────────────────────────────────────
        if "awswaf" in headers.get("Server","").lower() or "aws" in headers.get("X-Amzn-RequestId",""):
            if status == 403:
                return "AWS_WAF_BLOCK"

        # ── Sucuri ───────────────────────────────────────────────
        if "sucuri" in server or headers.get("X-Sucuri-ID"):
            if status in (403, 503):
                return "SUCURI_BLOCK"

        # ── Generic blocks ────────────────────────────────────────
        if status == 429:
            return "RATE_LIMIT"
        if status == 403 and any(kw in preview for kw in
            ["access denied", "forbidden", "blocked", "banned", "not allowed"]):
            return "GENERIC_403"
        if status == 503 and "bot" in preview:
            return "BOT_DETECTION"

        return None

    # ═══════════════════════════════════════════════════════════════
    # COOKIE HARVESTING
    # ═══════════════════════════════════════════════════════════════

    def absorb_cookies(self, domain: str, resp_headers: dict):
        """Extract WAF clearance cookies from response and persist them."""
        state = self._get_state(domain)
        raw   = resp_headers.get("Set-Cookie", "")
        if not raw:
            return
        # Handle multiple Set-Cookie headers (aiohttp joins with comma sometimes)
        for cookie_str in re.split(r",(?=[^;]+=[^;]+;)", raw):
            kv_part = cookie_str.strip().split(";")[0]
            if "=" not in kv_part:
                continue
            name, _, val = kv_part.partition("=")
            name = name.strip()
            val  = val.strip()
            for waf_name in WAF_COOKIE_NAMES:
                if name.startswith(waf_name) or name == waf_name:
                    state.cookies[name] = val
                    log.debug(f"[BYPASS] Stored cookie [{domain}] {name}={val[:20]}…")

    # ═══════════════════════════════════════════════════════════════
    # HUMAN-CADENCE TIMING
    # ═══════════════════════════════════════════════════════════════

    async def _delay(self, state: DomainState):
        """
        Poisson-distributed delay to mimic human browsing.
        Adapts based on domain's challenge history.
        """
        self._adapt_delay(state)
        base  = state.avg_delay
        # Poisson jitter: realistic inter-request timing
        jitter = random.expovariate(1.0 / max(0.1, base))
        jitter = min(jitter, base * 4)  # cap at 4x base
        await asyncio.sleep(jitter)

    # ═══════════════════════════════════════════════════════════════
    # MAIN BYPASS FETCH — ALL LAYERS COMBINED
    # ═══════════════════════════════════════════════════════════════

    async def fetch(
        self,
        url: str,
        *,
        retries: int = 5,
        timeout_total: float = 35,
        waf_hint: Optional[str] = None,
    ) -> Tuple[Optional[int], Optional[bytes], dict]:
        """
        Master bypass fetch.
        Fully autonomous: detects WAF, escalates strategy, rotates proxy,
        adapts delay, persists cookies — all automatically.
        """
        from yarl import URL
        domain = urlparse(url).netloc
        state  = self._get_state(domain)
        self._req_count += 1

        # Apply external WAF hint
        if waf_hint and not state.waf_type:
            state.waf_type = waf_hint

        last_err   = ""
        last_challenge = ""

        # Setup engine fallback
        use_cffi = False
        cffi_requests = None
        if state.strategy in ("SPOOF", "PROXY", "ROTATE"):
            try:
                from curl_cffi import requests
                cffi_requests = requests
                use_cffi = True
            except ImportError:
                pass

        for attempt in range(retries):
            await self._delay(state)

            # On ROTATE strategy: reset session fingerprint every attempt
            if state.strategy == "ROTATE":
                state.session_ua = None
                state.session_ip = None

            hdrs  = self.build_headers(url, state)
            tls   = self.make_tls_context(
                "firefox" if state.session_ua and "Firefox" in state.session_ua else "chrome"
            )

            # Proxy selection
            proxy = None
            if state.strategy in ("PROXY", "ROTATE") and self._proxy_list:
                proxy = self._pick_proxy(domain)
                if proxy:
                    log.debug(f"[BYPASS] Using proxy: {proxy}")

            # Try curl_cffi first if enabled for strategy
            if use_cffi and cffi_requests:
                try:
                    proxies_dict = {"http": proxy, "https": proxy} if proxy else None
                    async with cffi_requests.AsyncSession(
                        impersonate="chrome110", # Use a specific browser fingerprint
                        proxies=proxies_dict,
                        timeout=timeout_total,
                        headers=hdrs,
                        cookies=dict(state.cookies) # Pass existing cookies
                    ) as s:
                        resp = await s.get(url, allow_redirects=True)
                        body = resp.content
                        status = resp.status_code
                        resp_headers = dict(resp.headers)
                        # Sync cookies back to state
                        for k, v in resp.cookies.items():
                            state.cookies[k] = v

                    # If successful, process and return
                    self.absorb_cookies(domain, resp_headers)
                    state.referer = url
                    if not state.waf_type:
                        state.waf_type = U.detect_waf(resp_headers)
                    challenge = self.classify_challenge(status, body, resp_headers)

                    if challenge:
                        last_challenge = challenge
                        state.challenge_count += 1
                        log.warning(f"[BYPASS] {domain} → {challenge} (attempt {attempt+1}, strategy={state.strategy}, engine=cffi)")
                        self._record_failure(domain, challenge, proxy)
                        # Handle challenge-specific responses
                        if "RATE_LIMIT" in challenge or "429" in str(status):
                            wait = 8 + attempt * 4 + random.uniform(1, 3)
                            log.info(f"[BYPASS] Rate limited — waiting {wait:.1f}s")
                            await asyncio.sleep(wait)
                            continue
                        if "JS_CHALLENGE" in challenge or "TURNSTILE" in challenge:
                            await asyncio.sleep(5 + random.uniform(1, 3))
                            if proxy: self._record_failure(domain, challenge, proxy)
                            continue
                        if "CAPTCHA" in challenge:
                            state.session_ua = None; state.session_ip = None
                            await asyncio.sleep(3 + random.uniform(0.5, 2))
                            continue
                        if challenge in ("CF_403", "CF_BROWSER_CHECK", "CF_DIRECT_IP"):
                            await asyncio.sleep(2 + random.uniform(0.5, 1.5))
                            state.session_ip = None
                            continue
                        if "IMPERVA" in challenge or "DDOSGUARD" in challenge:
                            await asyncio.sleep(2 + random.uniform(0.5, 2))
                            continue
                        await asyncio.sleep(1.5) # Generic block
                        continue
                    else:
                        self._record_success(domain, proxy)
                        log.debug(f"[BYPASS] ✓ {domain} [{status}] attempt={attempt+1} strategy={state.strategy} (engine=cffi)")
                        return status, body, resp_headers

                except Exception as e:
                    last_err = f"cURL_CFFI Error: {e}"
                    log.debug(f"[BYPASS] cURL_CFFI failed, falling back to aiohttp: {e}")
                    # Fall through to aiohttp if cffi fails

            # aiohttp path (fallback or default)
            connector = aiohttp.TCPConnector(
                ssl=tls,
                limit=100,
                limit_per_host=15,
                ttl_dns_cache=600,
                enable_cleanup_closed=True,
            )
            timeout = aiohttp.ClientTimeout(
                total=timeout_total,
                connect=min(12.0, timeout_total * 0.4),
                sock_read=min(25.0, timeout_total * 0.7),
            )

            try:
                async with aiohttp.ClientSession(
                    connector=connector,
                    timeout=timeout,
                    headers=hdrs,
                    cookie_jar=aiohttp.CookieJar(unsafe=True, quote_cookie=False), # Use aiohttp's cookie jar
                ) as session:
                    # Inject gathered cookies into aiohttp's cookie jar
                    for k, v in state.cookies.items():
                        session.cookie_jar.update_cookies({k: v}, URL(url))

                    req_kwargs: dict = {
                        "allow_redirects": True,
                        "max_redirects":   15,
                    }
                    if proxy:
                        req_kwargs["proxy"] = proxy

                    async with session.get(url, **req_kwargs) as resp:
                        body   = await _safe_read_bytes(resp)
                        resp_h = dict(resp.headers)
                        status = resp.status

                        # Sync cookies back from aiohttp's cookie jar
                        for cookie in session.cookie_jar:
                            state.cookies[cookie.key] = cookie.value

                        # Harvest cookies
                        self.absorb_cookies(domain, resp_h)

                        # Update referer chain
                        state.referer = url

                        # Detect WAF from response
                        if not state.waf_type:
                            state.waf_type = U.detect_waf(resp_h)

                        # Classify challenge
                        challenge = self.classify_challenge(status, body, resp_h)

                        if challenge:
                            last_challenge = challenge
                            state.challenge_count += 1
                            log.warning(f"[BYPASS] {domain} → {challenge} (attempt {attempt+1}, strategy={state.strategy}, engine=aiohttp)")

                            self._record_failure(domain, challenge, proxy)

                            # Strategy-specific response
                            if "RATE_LIMIT" in challenge or "429" in str(status):
                                wait = 8 + attempt * 4 + random.uniform(1, 3)
                                log.info(f"[BYPASS] Rate limited — waiting {wait:.1f}s")
                                await asyncio.sleep(wait)
                                continue

                            if "JS_CHALLENGE" in challenge or "TURNSTILE" in challenge:
                                # JS challenge — can't solve without headless browser
                                # Best we can do: wait longer, rotate proxy
                                await asyncio.sleep(5 + random.uniform(1, 3))
                                if proxy:
                                    self._record_failure(domain, challenge, proxy)
                                continue

                            if "CAPTCHA" in challenge:
                                # Captcha — rotate everything and try fresh session
                                state.session_ua = None
                                state.session_ip = None
                                await asyncio.sleep(3 + random.uniform(0.5, 2))
                                continue

                            if challenge in ("CF_403", "CF_BROWSER_CHECK", "CF_DIRECT_IP"):
                                await asyncio.sleep(2 + random.uniform(0.5, 1.5))
                                state.session_ip = None  # rotate IP
                                continue

                            if "IMPERVA" in challenge or "DDOSGUARD" in challenge:
                                await asyncio.sleep(2 + random.uniform(0.5, 2))
                                continue

                            # Generic block: escalate and retry
                            await asyncio.sleep(1.5)
                            continue

                        # ── Clean response ────────────────────────────────────
                        self._record_success(domain, proxy)
                        if proxy:
                            self._proxy_records[proxy].success += 1
                        log.debug(f"[BYPASS] ✓ {domain} [{status}] attempt={attempt+1} strategy={state.strategy} (engine=aiohttp)")
                        return status, body, resp_h

            except aiohttp.ClientHttpProxyError as e:
                last_err = f"ProxyError: {e}"
                if proxy and proxy in self._proxy_records:
                    self._proxy_records[proxy].alive = False
                    self._proxy_records[proxy].failures += 1
                    if proxy in self._proxy_list:
                        self._proxy_list.remove(proxy)
                    log.debug(f"[BYPASS] Killed dead proxy: {proxy}")
            except aiohttp.ClientConnectorError as e:
                last_err = f"ConnectorError: {e}"
            except aiohttp.ServerDisconnectedError as e:
                last_err = f"Disconnected: {e}"
                await asyncio.sleep(1 + attempt * 0.5)
            except aiohttp.ClientResponseError as e:
                last_err = f"ResponseError {e.status}: {e.message}"
            except aiohttp.TooManyRedirects:
                last_err = "TooManyRedirects"
            except asyncio.TimeoutError:
                last_err = "Timeout"
                await asyncio.sleep(min(2 + attempt, 8))
            except Exception as e:
                last_err = str(e)
            finally:
                try:
                    await connector.close()
                except Exception:
                    pass

            self._record_failure(domain, last_err or "unknown", proxy)
            log.debug(f"[BYPASS] Attempt {attempt+1}/{retries} failed: {last_err or last_challenge}")

        log.warning(f"[BYPASS] Exhausted {retries} attempts for {url} | last={last_err or last_challenge}")
        return None, None, {}

    # ═══════════════════════════════════════════════════════════════
    # STATS
    # ═══════════════════════════════════════════════════════════════

    def stats(self) -> dict:
        alive_proxies = sum(1 for r in self._proxy_records.values() if r.alive)
        return {
            "total_requests":   self._req_count,
            "total_bypassed":   self._total_bypassed,
            "total_blocked":    self._total_blocked,
            "bypass_rate":      f"{self._total_bypassed / max(1, self._req_count) * 100:.1f}%",
            "proxy_total":      len(self._proxy_records),
            "proxy_alive":      alive_proxies,
            "domains_tracked":  len(self._domain_states),
            "strategies":       {d: s.strategy for d, s in self._domain_states.items()},
            "cookie_domains":   list(self._domain_states.keys()),
        }

    def domain_report(self, domain: str) -> Optional[DomainState]:
        return self._domain_states.get(domain)


# Global singleton
BYPASS = BypassEngine()




# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# RESILIENT SESSION FACTORY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _make_connector(ssl_verify: bool = False) -> aiohttp.TCPConnector:
    """Create a TCPConnector with generous limits and optional SSL bypass."""
    return aiohttp.TCPConnector(
        ssl=False,          # never verify SSL — avoids cert errors on mirrors
        limit=50,
        limit_per_host=10,
        ttl_dns_cache=300,
        enable_cleanup_closed=True,
        force_close=False,
    )

def _make_timeout(total: float = 30, connect: float = 10) -> aiohttp.ClientTimeout:
    return aiohttp.ClientTimeout(total=total, connect=connect, sock_read=20)

async def _safe_read_text(response: aiohttp.ClientResponse) -> str:
    """
    Multi-fallback text reader.
    Handles: bad Content-Encoding, unknown charset, binary bodies.
    Never raises — always returns a string.
    """
    # 1. Try normal aiohttp decode
    try:
        return await response.text(errors="replace")
    except Exception:
        pass
    # 2. Read raw bytes, decode manually
    try:
        raw = await response.read()
    except Exception:
        return ""
    # 3. Try to decompress if server lied about encoding
    for codec in ("utf-8", "latin-1", "cp1252", "iso-8859-1"):
        try:
            return raw.decode(codec, errors="replace")
        except Exception:
            continue
    # 4. Last resort
    return raw.decode("ascii", errors="replace")

async def _safe_read_bytes(response: aiohttp.ClientResponse) -> bytes:
    """
    Raw bytes reader with fallback.
    Bypasses aiohttp's content-encoding decompression entirely.
    """
    try:
        return await response.read()
    except Exception:
        # Try reading the raw stream directly
        try:
            chunks = []
            async for chunk in response.content.iter_any():
                chunks.append(chunk)
            return b"".join(chunks)
        except Exception:
            return b""

async def _fetch_with_retry(
    url: str,
    *,
    retries: int = 4,
    timeout_total: float = 35,
    return_bytes: bool = False,
    extra_headers: dict = None,
    waf_hint: Optional[str] = None,
) -> Tuple[Optional[int], Optional[bytes], dict]:
    """
    Universal fetch — routes through the global BYPASS engine.
    Handles: Cloudflare, Imperva, DDoS-Guard, Akamai, rate-limiting,
    cookie challenges, IP blocks, TLS fingerprinting, proxy rotation.
    Never raises — always returns (status, bytes, headers).
    """
    # BYPASS engine not yet initialised (called before global is set) → fallback
    try:
        bypass = BYPASS
    except NameError:
        bypass = None

    if bypass is not None:
        return await bypass.fetch(
            url,
            retries=retries,
            timeout_total=timeout_total,
            waf_hint=waf_hint,
        )

    # Bare fallback (should never happen after module init)
    last_err = ""
    for attempt in range(retries):
        if attempt > 0:
            await asyncio.sleep(0.5 * (2 ** attempt) + random.uniform(0, 0.5))
        connector = _make_connector()
        timeout   = _make_timeout(total=timeout_total)
        hdrs      = get_stealth_headers(extra_headers)
        try:
            async with aiohttp.ClientSession(
                connector=connector, timeout=timeout, headers=hdrs,
            ) as session:
                async with session.get(url, allow_redirects=True, max_redirects=10) as resp:
                    body = await _safe_read_bytes(resp)
                    return resp.status, body, dict(resp.headers)
        except Exception as e:
            last_err = str(e)
        finally:
            try:
                await connector.close()
            except Exception:
                pass
    return None, None, {}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DATA MODELS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@dataclass
class TargetIntel:
    url: str
    domain: str
    ip: str                       = "—"
    asn: str                      = "—"
    org: str                      = "—"
    country: str                  = "—"
    city: str                     = "—"
    server: str                   = "—"
    latency_ms: int               = 0
    ssl_issuer: str               = "—"
    ssl_expiry: str               = "—"
    ssl_grade: str                = "—"
    tls_version: str              = "—"
    http_version: str             = "—"
    headers: Dict                 = field(default_factory=dict)
    cookies: Dict                 = field(default_factory=dict)
    security_headers: Dict        = field(default_factory=dict)
    missing_sec_headers: List     = field(default_factory=list)
    technologies: List[str]       = field(default_factory=list)
    cms: str                      = "Unknown"
    robots_txt: Optional[str]     = None
    sitemap_urls: List[str]       = field(default_factory=list)
    open_ports: List[Tuple]       = field(default_factory=list)   # (port, banner)
    subdomains: List[str]         = field(default_factory=list)
    emails: List[str]             = field(default_factory=list)
    js_files: List[str]           = field(default_factory=list)
    forms: List[Dict]             = field(default_factory=list)
    comments: List[str]           = field(default_factory=list)
    status_code: int              = 0
    redirect_chain: List[str]     = field(default_factory=list)
    waf_detected: Optional[str]   = None
    cdn_detected: Optional[str]   = None
    scan_time: float              = field(default_factory=time.time)
    score: int                    = 0   # computed security score 0-100
    # New fields for live layout
    target_url: str               = ""
    bandwidth_usage: float        = 0.0


@dataclass
class ArchiveSession:
    session_id: str
    target: str
    mode: str
    start_time: float
    files_count: int          = 0
    bytes_downloaded: int     = 0
    errors: List[str]         = field(default_factory=list)
    warnings: List[str]       = field(default_factory=list)
    status: str               = "INIT"
    completed_urls: Set[str]  = field(default_factory=set)
    failed_urls: Set[str]     = field(default_factory=set)
    pending_urls: deque       = field(default_factory=deque)
    speed_samples: deque      = field(default_factory=lambda: deque(maxlen=20))
    output_dir: Optional[Path]= None
    # New fields for live layout
    active_workers: int       = 0
    concurrency: int          = 0
    requests_sent: int        = 0

    @property
    def elapsed(self) -> float:
        return time.time() - self.start_time

    @property
    def avg_speed(self) -> float:
        if not self.speed_samples:
            return 0.0
        return sum(self.speed_samples) / len(self.speed_samples)

    @property
    def eta_seconds(self) -> Optional[int]:
        pending = len(self.pending_urls)
        if self.avg_speed > 0 and pending > 0:
            return int(pending / self.avg_speed)
        return None

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# UTILITIES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class U:
    @staticmethod
    def ts() -> str:
        return datetime.datetime.now().strftime("%H:%M:%S")

    @staticmethod
    def stamp() -> str:
        return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    @staticmethod
    def uid(prefix="NX") -> str:
        return f"{prefix}-{uuid.uuid4().hex[:10].upper()}"

    @staticmethod
    def size(b: int) -> str:
        for unit in ("B","KB","MB","GB","TB"):
            if b < 1024:
                return f"{b:.1f} {unit}"
            b /= 1024
        return f"{b:.1f} PB"

    @staticmethod
    def clean_url(raw: str) -> str:
        raw = raw.strip()
        if not raw.startswith(("http://","https://")):
            raw = "https://" + raw
        return raw.rstrip("/")

    @staticmethod
    def safe_fname(s: str) -> str:
        return re.sub(r"[^\w\-.]", "_", s)[:200]

    @staticmethod
    def hash_file(path: Path, algo: str = "sha256") -> str:
        h = hashlib.new(algo)
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()

    @staticmethod
    def extract_emails(text: str) -> List[str]:
        return list(set(re.findall(
            r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", text
        )))

    @staticmethod
    def detect_waf(headers: dict) -> Optional[str]:
        waf_sigs = {
            "cloudflare":    ["cf-ray", "cf-cache-status", "cloudflare"],
            "akamai":        ["x-akamai-transformed", "akamai"],
            "imperva":       ["x-cdn", "imperva", "incapsula"],
            "aws-shield":    ["x-amzn-requestid", "x-amz-"],
            "sucuri":        ["x-sucuri-id", "sucuri"],
            "f5-big-ip":    ["x-waf-status", "bigip", "f5"],
        }
        combined = " ".join(f"{k.lower()}:{v.lower()}" for k, v in headers.items())
        for name, sigs in waf_sigs.items():
            if any(sig in combined for sig in sigs):
                return name.upper()
        return None

    @staticmethod
    def detect_cdn(headers: dict) -> Optional[str]:
        cdn_sigs = {
            "Cloudflare":  ["cf-ray"],
            "Fastly":      ["x-fastly-request-id","fastly"],
            "Varnish":     ["x-varnish","via"],
            "CloudFront":  ["x-amz-cf-id","cloudfront"],
            "BunnyCDN":    ["bunny-request-id"],
        }
        combined = " ".join(f"{k.lower()}:{v.lower()}" for k, v in headers.items())
        for name, sigs in cdn_sigs.items():
            if any(sig in combined for sig in sigs):
                return name
        return None

    @staticmethod
    def detect_cms(headers: dict, html: str) -> str:
        checks = {
            "WordPress":  ["wp-content","wp-includes","wordpress"],
            "Drupal":     ["drupal","drupal.org"],
            "Joomla":     ["/components/com_","joomla"],
            "Shopify":    ["cdn.shopify.com","shopify"],
            "Wix":        ["static.wixstatic.com","wix.com"],
            "Squarespace":["squarespace.com"],
            "Ghost":      ["ghost.io","ghost-theme"],
            "Magento":    ["magento","varien"],
        }
        body = html.lower()
        hdrs = " ".join(v.lower() for v in headers.values())
        for cms, sigs in checks.items():
            if any(s in body or s in hdrs for s in sigs):
                return cms
        return "Unknown"

    @staticmethod
    def security_score(intel: "TargetIntel") -> int:
        score = 100
        required = {
            "Strict-Transport-Security": -20,
            "Content-Security-Policy":   -20,
            "X-Frame-Options":           -10,
            "X-Content-Type-Options":    -10,
            "Permissions-Policy":        -10,
        }
        for h, penalty in required.items():
            if h not in intel.security_headers:
                score += penalty
                intel.missing_sec_headers.append(h)
        if not intel.url.startswith("https"):
            score -= 20
        if intel.waf_detected:
            score += 10
        return max(0, min(100, score))

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SYSTEM PULSE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class SystemPulse:
    def __init__(self):
        self._t0     = time.time()
        self._proc   = psutil.Process(os.getpid())
        self._net0   = psutil.net_io_counters()
        self.peak_cpu = 0.0
        self.peak_mem = 0.0
        self._hist   = deque(maxlen=30)

    def sample(self) -> dict:
        net = psutil.net_io_counters()
        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory()
        self.peak_cpu = max(self.peak_cpu, cpu)
        self.peak_mem = max(self.peak_mem, mem.percent)
        d = {
            "cpu":        cpu,
            "cpu_peak":   self.peak_cpu,
            "mem_pct":    mem.percent,
            "mem_peak":   self.peak_mem,
            "mem_total":  U.size(mem.total),
            "mem_avail":  U.size(mem.available),
            "net_rx":     U.size(net.bytes_recv - self._net0.bytes_recv) + "/s",
            "net_tx":     U.size(net.bytes_sent - self._net0.bytes_sent) + "/s",
            "uptime":     str(datetime.timedelta(seconds=int(time.time()-self._t0))),
            "threads":    threading.active_count(),
            "proc_mem":   U.size(self._proc.memory_info().rss),
            "fd_count":   self._proc.num_fds() if hasattr(self._proc, "num_fds") else "N/A",
        }
        self._net0 = net
        self._hist.append(d)
        return d

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ADVANCED RECON ENGINE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COMMON_PORTS = [
    (21,"FTP"),(22,"SSH"),(23,"Telnet"),(25,"SMTP"),(53,"DNS"),
    (80,"HTTP"),(110,"POP3"),(143,"IMAP"),(443,"HTTPS"),(445,"SMB"),
    (3306,"MySQL"),(5432,"PostgreSQL"),(6379,"Redis"),(8080,"HTTP-Alt"),
    (8443,"HTTPS-Alt"),(27017,"MongoDB"),
]

SEC_HEADERS_REQUIRED = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "X-XSS-Protection",
    "Referrer-Policy",
    "Permissions-Policy",
    "Cross-Origin-Opener-Policy",
]

class ReconEngine:
    """
    Full-stack reconnaissance engine.
    Modules: DNS, GeoIP, HTTP, SSL/TLS, Security Headers,
             WAF/CDN detection, CMS fingerprint, Tech detection,
             Passive port scan, Subdomain enumeration,
             robots/sitemap, HTML deep parse.
    """

    SUBDOMAIN_WORDLIST = [
        "www","mail","ftp","admin","api","dev","staging","blog","shop",
        "cdn","img","static","media","assets","vpn","remote","portal",
        "app","dashboard","beta","test","old","new","secure","internal",
        "mx","ns1","ns2","smtp","pop","imap","webmail","m",
    ]

    def __init__(self, url: str):
        self.url    = U.clean_url(url)
        self.domain = urlparse(self.url).netloc.split(":")[0]
        self.intel  = TargetIntel(url=self.url, domain=self.domain, target_url=self.url)
        self._raw_html = ""

    async def run(self, deep: bool = False) -> TargetIntel:
        tasks = [
            self._dns(),
            self._http_probe(),
            self._ssl(),
            self._robots_sitemap(),
        ]
        await asyncio.gather(*tasks, return_exceptions=True)

        # Second pass — needs html
        await asyncio.gather(
            self._deep_parse(),
            self._subdomain_enum() if deep else asyncio.sleep(0),
            self._port_scan() if deep else asyncio.sleep(0),
            return_exceptions=True,
        )

        # Derived metrics
        self.intel.score = U.security_score(self.intel)
        log.info(f"Recon complete for {self.domain} — score {self.intel.score}/100")
        return self.intel

    # ── DNS & GeoIP ──────────────────────────────────────────────────────────
    async def _dns(self):
        try:
            self.intel.ip = socket.gethostbyname(self.domain)
        except Exception as e:
            log.warning(f"DNS failed: {e}")
            self.intel.ip = "UNRESOLVED"
            return
        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(
                    f"http://ip-api.com/json/{self.intel.ip}?fields=status,country,city,org,as",
                    timeout=aiohttp.ClientTimeout(total=5),
                ) as r:
                    d = await r.json()
                    if d.get("status") == "success":
                        self.intel.country = d.get("country","—")
                        self.intel.city    = d.get("city","—")
                        self.intel.org     = d.get("org","—")
                        self.intel.asn     = d.get("as","—")
        except Exception as e:
            log.debug(f"GeoIP failed: {e}")

    # ── HTTP probe ────────────────────────────────────────────────────────────
    async def _http_probe(self):
        t0 = time.time()
        # Use bypass engine — handles Cloudflare, Imperva, rate-limits, etc.
        status, body, headers = await BYPASS.fetch(
            self.url, retries=4, timeout_total=25, waf_hint=None,
        )
        if status is None or body is None:
            log.warning(f"HTTP probe failed for {self.url}")
            return

        self.intel.latency_ms   = int((time.time() - t0) * 1000)
        self.intel.status_code  = status
        self.intel.headers      = headers
        self.intel.server       = headers.get("Server", "—")
        self.intel.http_version = "1.1"
        self.intel.waf_detected = U.detect_waf(headers)
        self.intel.cdn_detected = U.detect_cdn(headers)

        # If WAF detected, retry with targeted bypass headers
        if self.intel.waf_detected and (status is None or status >= 400):
            log.info(f"[BYPASS] Re-probing with WAF hint: {self.intel.waf_detected}")
            status2, body2, headers2 = await BYPASS.fetch(
                self.url, retries=3, timeout_total=25, waf_hint=self.intel.waf_detected,
            )
            if body2:
                status, body, headers = status2, body2, headers2

        # Security headers
        for h in SEC_HEADERS_REQUIRED:
            if h in headers:
                self.intel.security_headers[h] = headers[h][:80]

        # Tech from headers
        for hdr in ["X-Powered-By","X-Generator","X-Drupal-Cache","X-Shopify-Stage"]:
            if hdr in headers:
                self.intel.technologies.append(f"{hdr}: {headers[hdr]}")

        # Decode HTML
        for enc in ("utf-8", "latin-1", "cp1252", "iso-8859-1"):
            try:
                self._raw_html = body.decode(enc, errors="replace")
                break
            except Exception:
                continue
        else:
            self._raw_html = body.decode("ascii", errors="replace")

        self.intel.cms = U.detect_cms(headers, self._raw_html)

    # ── SSL/TLS ───────────────────────────────────────────────────────────────
    async def _ssl(self):
        if not self.url.startswith("https"):
            return
        try:
            ctx = ssl.create_default_context()
            loop = asyncio.get_event_loop()
            def _sync():
                with socket.create_connection((self.domain,443), timeout=6) as sock:
                    with ctx.wrap_socket(sock, server_hostname=self.domain) as ss:
                        cert = ss.getpeercert()
                        issuer = dict(x[0] for x in cert.get("issuer",[])).get("organizationName","—")
                        expiry = cert.get("notAfter","")
                        exp_dt = datetime.datetime.strptime(expiry, "%b %d %H:%M:%S %Y %Z") if expiry else None
                        return issuer, exp_dt.strftime("%Y-%m-%d") if exp_dt else "—", ss.version()
            issuer, expiry, tls = await loop.run_in_executor(None, _sync)
            self.intel.ssl_issuer  = issuer
            self.intel.ssl_expiry  = expiry
            self.intel.tls_version = tls or "—"

            # Grade
            if tls and "1.3" in tls:
                self.intel.ssl_grade = "A+"
            elif tls and "1.2" in tls:
                self.intel.ssl_grade = "B"
            else:
                self.intel.ssl_grade = "C"
        except Exception as e:
            log.debug(f"SSL error: {e}")

    # ── robots.txt & sitemap ──────────────────────────────────────────────────
    async def _robots_sitemap(self):
        for path in ["/robots.txt"]:
            status, body, _ = await BYPASS.fetch(
                f"{self.url}{path}", retries=2, timeout_total=8,
            )
            if status == 200 and body:
                for enc in ("utf-8","latin-1"):
                    try:
                        self.intel.robots_txt = body.decode(enc, errors="replace")
                        break
                    except Exception:
                        pass

        for path in ["/sitemap.xml", "/sitemap_index.xml", "/sitemap.gz"]:
            status, _, _ = await BYPASS.fetch(
                f"{self.url}{path}", retries=1, timeout_total=6,
            )
            if status == 200:
                self.intel.sitemap_urls.append(f"{self.url}{path}")

    # ── Deep HTML Parse ───────────────────────────────────────────────────────
    async def _deep_parse(self):
        if not self._raw_html:
            return
        try:
            soup = BeautifulSoup(self._raw_html, "lxml")

            # Emails
            self.intel.emails = U.extract_emails(self._raw_html)

            # JS files
            self.intel.js_files = [
                s.get("src","") for s in soup.find_all("script",src=True)
            ][:20]

            # Forms
            for form in soup.find_all("form"):
                inputs = [i.get("name","?") for i in form.find_all("input")]
                self.intel.forms.append({
                    "action": form.get("action",""),
                    "method": form.get("method","GET"),
                    "inputs": inputs,
                })

            # HTML comments (leak hunting)
            import re as _re
            comments = _re.findall(r"<!--(.*?)-->", self._raw_html, re.DOTALL)
            self.intel.comments = [c.strip() for c in comments if len(c.strip()) > 5][:10]

            # Meta generator
            gen = soup.find("meta", attrs={"name": re.compile("generator", re.I)})
            if gen and gen.get("content"):
                self.intel.technologies.append(f"Generator: {gen['content']}")

        except Exception as e:
            log.debug(f"Deep parse error: {e}")

    # ── Subdomain Enum ────────────────────────────────────────────────────────
    async def _subdomain_enum(self):
        found = []
        base = ".".join(self.domain.split(".")[-2:])

        async def _try(sub):
            full = f"{sub}.{base}"
            try:
                loop = asyncio.get_event_loop()
                ip = await loop.run_in_executor(None, socket.gethostbyname, full)
                found.append(f"{full} → {ip}")
            except: pass

        tasks = [_try(s) for s in self.SUBDOMAIN_WORDLIST]
        await asyncio.gather(*tasks)
        self.intel.subdomains = found

    # ── Port Scan ─────────────────────────────────────────────────────────────
    async def _port_scan(self):
        if self.intel.ip in ("UNRESOLVED","—"):
            return
        open_ports = []

        async def _probe(port, svc):
            try:
                future = asyncio.open_connection(self.intel.ip, port)
                reader, writer = await asyncio.wait_for(future, timeout=1.5)
                banner = ""
                try:
                    data = await asyncio.wait_for(reader.read(256), timeout=1.0)
                    banner = data.decode(errors="replace").strip()[:60]
                except: pass
                writer.close()
                open_ports.append((port, svc, banner))
            except: pass

        tasks = [_probe(p, s) for p, s in COMMON_PORTS]
        await asyncio.gather(*tasks)
        self.intel.open_ports = sorted(open_ports, key=lambda x: x[0])

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ASYNC DOWNLOAD ENGINE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MODES = {
    "SINGLE":    {"depth": 0, "concurrent": 5,  "desc": "Download single resource"},
    "CRAWL":     {"depth": 2, "concurrent": 15, "desc": "Crawl & archive (depth 2)"},
    "DEEP":      {"depth": 4, "concurrent": 20, "desc": "Deep crawl (depth 4)"},
    "MIRROR":    {"depth": 6, "concurrent": 30, "desc": "Full site mirror (depth 6)"},
    "SITEMAP":   {"depth": 0, "concurrent": 20, "desc": "Sitemap-driven bulk download"},
}

class DownloadEngine:
    def __init__(self, target: str, mode: str, intel: TargetIntel):
        self.target  = U.clean_url(target)
        self.mode    = mode.upper()
        self.intel   = intel
        self.cfg     = MODES.get(self.mode, MODES["CRAWL"])
        self.session = ArchiveSession(
            session_id=U.uid("ARCH"),
            target=self.target,
            mode=self.mode,
            start_time=time.time(),
            concurrency=int(self.cfg["concurrent"]) # Initialize concurrency
        )
        folder = f"{urlparse(self.target).netloc}_{U.stamp()}"
        self.session.output_dir = ARCH / folder
        self.session.output_dir.mkdir(parents=True, exist_ok=True)
        self._sem     = None
        self._visited: Set[str] = set()
        self._lock    = asyncio.Lock()
        self._stop    = False
        self._t_last  = time.time()
        self._b_last  = 0

    # ── Main entry ────────────────────────────────────────────────────────────
    async def run(self):
        self._sem = asyncio.Semaphore(self.cfg["concurrent"])
        self.session.status = "RUNNING"
        try:
            if self.mode == "SITEMAP" and self.intel.sitemap_urls:
                await self._run_sitemap()
            else:
                await self._run_crawl(self.target, 0)
        except asyncio.CancelledError:
            pass
        finally:
            self.session.status = "DONE"

    async def _run_crawl(self, start: str, start_depth: int):
        """BFS crawl with semaphore-limited parallel fetch."""
        queue   = asyncio.Queue()
        await queue.put((start, start_depth))
        tasks   = set()
        max_d   = self.cfg["depth"]

        async def worker():
            while not self._stop:
                try:
                    url, depth = queue.get_nowait()
                except asyncio.QueueEmpty:
                    await asyncio.sleep(0.05)
                    if queue.empty() and not tasks:
                        break
                    continue
                async with self._lock:
                    if url in self._visited:
                        queue.task_done()
                        continue
                    self._visited.add(url)
                self.session.active_workers += 1 # Increment active workers
                async with self._sem:
                    links = await self._fetch(url)
                self.session.active_workers -= 1 # Decrement active workers
                if depth < max_d:
                    for link in links:
                        if link not in self._visited:
                            await queue.put((link, depth+1))
                queue.task_done()

        workers = [asyncio.create_task(worker()) for _ in range(self.cfg["concurrent"])]
        tasks.update(workers)
        await asyncio.gather(*workers, return_exceptions=True)

    async def _run_sitemap(self):
        """Download via sitemap URLs."""
        for sm_url in self.intel.sitemap_urls:
            status, body, _ = await BYPASS.fetch(sm_url, retries=2, timeout_total=12)
            if status == 200 and body:
                for enc in ("utf-8","latin-1"):
                    try:
                        xml = body.decode(enc, errors="replace")
                        break
                    except Exception:
                        xml = ""
                urls = re.findall(r"<loc>(.*?)</loc>", xml)
                log.info(f"Sitemap {sm_url}: {len(urls)} URLs")
                tasks = [self._fetch(u.strip()) for u in urls if u.strip()]
                await asyncio.gather(*tasks, return_exceptions=True)

    async def _fetch(self, url: str) -> List[str]:
        """
        Fetch a single URL with full resilience:
        - 3 retries with backoff
        - Accept-Encoding: identity (no decode errors)
        - Stealth headers rotation
        - Safe bytes read (never raises on encoding)
        - Save raw bytes to disk (no decode needed)
        - Extract links from decoded HTML
        """
        # Remove from pending
        self.session.pending_urls = deque(
            [u for u in self.session.pending_urls if u != url]
        )
        self.session.requests_sent += 1 # Increment requests sent

        async with self._sem:
            status, body, resp_headers = await BYPASS.fetch(
                url, retries=3, timeout_total=35,
                waf_hint=self.intel.waf_detected if self.intel else None,
            )

        if status is None or body is None:
            self.session.failed_urls.add(url)
            self.session.errors.append(f"UNREACHABLE: {url}")
            return []

        if status not in (200, 206, 301, 302):
            # Log non-fatal HTTP errors but don't crash
            self.session.warnings.append(f"HTTP {status}: {url}")
            if status >= 400:
                self.session.failed_urls.add(url)
                return []

        ctype = resp_headers.get("Content-Type", "")
        # Extract and rewrite links if HTML
        if "text/html" in ctype or url.endswith((".html", ".htm", "/")):
            body, extracted_links = self._extract_and_rewrite(body, url)
        else:
            extracted_links = []

        # Save to disk
        try:
            filepath = self._url_to_path(url)
            filepath.parent.mkdir(parents=True, exist_ok=True)
            filepath.write_bytes(body)
        except OSError as e:
            # Path too long or permission error — use flat fallback with proper extension
            try:
                ext = Path(urlparse(url).path).suffix or ".html"
                if not ext.startswith("."): ext = ".html"
                if len(ext) > 10: ext = ".html"
                hash_full = hashlib.md5(url.encode()).hexdigest()
                hash_short = ""
                for i in range(12): hash_short += hash_full[i]
                fallback = self.session.output_dir / f"_{hash_short}{ext}"
                fallback.write_bytes(body)
                filepath = fallback
            except Exception as fe:
                self.session.errors.append(f"SAVE_ERR: {url}: {fe}")
                return []

        size = len(body)
        self.session.files_count      += 1
        self.session.bytes_downloaded += size
        self.session.completed_urls.add(url)

        # Speed tracking
        now = time.time()
        dt  = now - self._t_last
        if dt >= 0.5:
            speed = (self.session.bytes_downloaded - self._b_last) / dt
            self.session.speed_samples.append(speed)
            self._t_last = now
            self._b_last = self.session.bytes_downloaded
        self.intel.bandwidth_usage = self.session.avg_speed # Update intel bandwidth

        log.info(f"[{status}] {url} → {filepath.name} ({U.size(size)})")

        return extracted_links

    def _url_to_path(self, url: str) -> Path:
        """
        Convert URL to safe local path.
        Handles: empty paths, very long paths, special chars, query strings.
        """
        try:
            parsed = urlparse(url)
            # Strip query string from path for filename
            path   = parsed.path.strip("/")
            if not path:
                path = "index.html"

            parts = [U.safe_fname(p) for p in path.split("/") if p]
            if not parts:
                parts = ["index.html"]

            # Ensure last part has extension
            last = parts[-1]
            if "." not in last:
                last = last + ".html" if last else "index.html"
                parts[-1] = last

            base  = self.session.output_dir / U.safe_fname(parsed.netloc)
            final = base.joinpath(*parts)

            # Clamp total path length (Windows: 260, Linux: 4096)
            if len(str(final)) > 240:
                ext  = Path(last).suffix or ".html"
                name = hashlib.md5(url.encode()).hexdigest()[:16] + ext
                final = self.session.output_dir / U.safe_fname(parsed.netloc) / name

            return final
        except Exception:
            # Absolute fallback
            fname = hashlib.md5(url.encode()).hexdigest() + ".html"
            return self.session.output_dir / fname

    def _extract_and_rewrite(self, html: bytes, base: str) -> Tuple[bytes, List[str]]:
        """
        Safely extract all in-domain links from raw HTML bytes and rewrite them.
        Rewrites absolute/relative URLs to be local relative paths for true offline viewing.
        """
        try:
            # Decode bytes safely
            for enc in ("utf-8", "latin-1", "cp1252"):
                try:
                    text = html.decode(enc, errors="replace")
                    break
                except Exception:
                    text = ""

            soup   = BeautifulSoup(text, "lxml")
            base_d = urlparse(self.target).netloc
            links  = set()
            base_path = self._url_to_path(base)

            for tag in soup.find_all(["a","img","script","link","video","source","iframe","form"]):
                for attr in ("href","src","action","data-src"):
                    href = tag.get(attr, "")
                    if not href or not isinstance(href, str):
                        continue
                    href = href.strip()
                    if href.startswith(("mailto:","tel:","javascript:","data:","#","")):
                        continue
                    try:
                        abs_url = urljoin(base, href)
                        parsed  = urlparse(abs_url)
                        # Only same domain, only http/https
                        if parsed.scheme not in ("http","https"):
                            continue
                        if parsed.netloc != base_d:
                            continue
                        # Strip fragment and normalize
                        clean = abs_url.split("#")[0]
                        links.add(clean)

                        # Offline Rewrite Magic
                        target_path = self._url_to_path(clean)
                        try:
                            rel_path = os.path.relpath(target_path, base_path.parent)
                            rel_path = rel_path.replace("\\", "/") # cross-platform web compat
                            tag[attr] = rel_path
                        except ValueError:
                            pass # if relation fails somehow

                    except Exception:
                        continue

            return str(soup).encode("utf-8", errors="replace"), list(links)
        except Exception as e:
            log.debug(f"Link extraction error: {e}")
            return html, []

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# REPORT GENERATOR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ReportGen:
    @staticmethod
    def html(intel: TargetIntel, session: ArchiveSession) -> Path:
        score = intel.score
        score_color = "#00ff41" if score >= 70 else "#ffb800" if score >= 40 else "#ff3c3c"
        out = REP / f"NEXUS_{U.safe_fname(intel.domain)}_{U.stamp()}.html"
        port_rows = "".join(
            f"<tr><td>{p}</td><td><b>{s}</b></td><td><code>{b or '—'}</code></td></tr>"
            for p,s,b in intel.open_ports
        ) or "<tr><td colspan='3'>No open ports detected</td></tr>"
        tech_items = "".join(f"<li>{t}</li>" for t in intel.technologies) or "<li>None detected</li>"
        sec_rows = "".join(
            f"<tr class='ok'><td>✔ {h}</td><td>{v[:80]}</td></tr>"
            for h,v in intel.security_headers.items()
        ) + "".join(
            f"<tr class='miss'><td>✘ {h}</td><td>MISSING</td></tr>"
            for h in intel.missing_sec_headers
        )
        form_rows = "".join(
            f"<tr><td>{f['action']}</td><td>{f['method']}</td><td>{', '.join(f['inputs'])}</td></tr>"
            for f in intel.forms
        ) or "<tr><td colspan='3'>No forms detected</td></tr>"
        subdomain_items = "".join(
            f"<li><code>{s}</code></li>" for s in intel.subdomains
        ) or "<li>None found</li>"
        email_items = "".join(f"<li>{e}</li>" for e in intel.emails) or "<li>None</li>"
        comment_items = "".join(
            f"<li><code>{c[:120]}</code></li>" for c in intel.comments
        ) or "<li>None</li>"
        redir_items = "".join(f"<li>{r}</li>" for r in intel.redirect_chain) or "<li>Direct (no redirects)</li>"

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>NEXUS REPORT — {intel.domain}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;600;700&display=swap');
  :root {{
    --bg:    #050a0e;
    --bg2:   #0a1520;
    --bg3:   #0f1e2e;
    --acc:   #00d4ff;
    --acc2:  #00ff41;
    --warn:  #ffb800;
    --err:   #ff3c3c;
    --text:  #c8d8e8;
    --dim:   #5a7080;
    --border:#1e3a4a;
  }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:var(--bg); color:var(--text); font-family:'Rajdhani',sans-serif; font-size:15px; line-height:1.6; }}
  body::before {{
    content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
    background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,212,255,.015) 2px,rgba(0,212,255,.015) 4px);
  }}
  .wrap {{ max-width:1300px; margin:0 auto; padding:30px 20px; position:relative; z-index:1; }}
  /* Header */
  .hdr {{ text-align:center; padding:40px 0 30px; border-bottom:2px solid var(--acc); margin-bottom:30px; }}
  .hdr h1 {{ font-size:2.8rem; color:var(--acc); letter-spacing:.2em; text-shadow:0 0 30px rgba(0,212,255,.5); }}
  .hdr .sub {{ color:var(--dim); letter-spacing:.15em; margin-top:8px; font-size:1rem; }}
  .hdr .meta {{ display:flex; justify-content:center; gap:30px; margin-top:20px; flex-wrap:wrap; }}
  .hdr .meta span {{ background:var(--bg3); border:1px solid var(--border); padding:6px 16px; border-radius:2px; font-family:'Share Tech Mono',monospace; font-size:.85rem; }}
  /* Score */
  .score-wrap {{ display:flex; justify-content:center; margin-bottom:30px; }}
  .score-ring {{ position:relative; width:160px; height:160px; }}
  .score-ring svg {{ transform:rotate(-90deg); }}
  .score-ring .val {{ position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; }}
  .score-ring .val .num {{ font-size:2.5rem; font-weight:700; color:{score_color}; font-family:'Share Tech Mono',monospace; text-shadow:0 0 20px {score_color}; }}
  .score-ring .val .lbl {{ font-size:.7rem; letter-spacing:.15em; color:var(--dim); }}
  /* Grid */
  .grid2 {{ display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:20px; }}
  .grid3 {{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:20px; margin-bottom:20px; }}
  @media(max-width:900px) {{ .grid2,.grid3 {{ grid-template-columns:1fr; }} }}
  /* Card */
  .card {{ background:var(--bg2); border:1px solid var(--border); padding:20px; position:relative; overflow:hidden; }}
  .card::before {{ content:''; position:absolute; top:0; left:0; right:0; height:2px; background:linear-gradient(90deg,var(--acc),var(--acc2)); }}
  .card h2 {{ font-size:1.1rem; color:var(--acc); letter-spacing:.15em; text-transform:uppercase; margin-bottom:15px; padding-bottom:8px; border-bottom:1px solid var(--border); }}
  /* Table */
  table {{ width:100%; border-collapse:collapse; font-size:.9rem; }}
  th {{ background:var(--bg3); color:var(--acc); padding:8px 12px; text-align:left; font-size:.75rem; letter-spacing:.1em; text-transform:uppercase; }}
  td {{ padding:8px 12px; border-bottom:1px solid var(--border); vertical-align:top; }}
  tr:last-child td {{ border-bottom:none; }}
  td:first-child {{ color:var(--acc); font-family:'Share Tech Mono',monospace; font-size:.85rem; white-space:nowrap; }}
  tr.ok td {{ color:var(--acc2); }}
  tr.ok td:first-child {{ color:var(--acc2); }}
  tr.miss td {{ color:var(--err); opacity:.8; }}
  tr.miss td:first-child {{ color:var(--err); }}
  code {{ background:rgba(0,212,255,.08); color:var(--acc2); padding:1px 6px; border-radius:2px; font-family:'Share Tech Mono',monospace; font-size:.8rem; }}
  ul {{ list-style:none; }}
  li {{ padding:4px 0; border-bottom:1px solid var(--border); font-family:'Share Tech Mono',monospace; font-size:.82rem; }}
  li:last-child {{ border-bottom:none; }}
  /* Badges */
  .badge {{ display:inline-block; padding:2px 10px; border-radius:2px; font-size:.75rem; font-weight:700; letter-spacing:.1em; }}
  .badge-g {{ background:rgba(0,255,65,.15); color:var(--acc2); border:1px solid var(--acc2); }}
  .badge-y {{ background:rgba(255,184,0,.15); color:var(--warn); border:1px solid var(--warn); }}
  .badge-r {{ background:rgba(255,60,60,.15); color:var(--err); border:1px solid var(--err); }}
  .badge-b {{ background:rgba(0,212,255,.15); color:var(--acc); border:1px solid var(--acc); }}
  /* Footer */
  footer {{ text-align:center; padding:30px 0; color:var(--dim); font-size:.8rem; border-top:1px solid var(--border); margin-top:30px; font-family:'Share Tech Mono',monospace; }}
</style>
</head>
<body>
<div class="wrap">
  <div class="hdr">
    <h1>◈ NEXUS INTEL REPORT ◈</h1>
    <div class="sub">TITAN OMEGA v8.0 — SOVEREIGN EDITION // 2026</div>
    <div class="meta">
      <span>TARGET: {intel.domain}</span>
      <span>SESSION: {session.session_id}</span>
      <span>GENERATED: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
      <span>MODE: {session.mode}</span>
    </div>
  </div>

  <div class="score-wrap">
    <div class="score-ring">
      <svg width="160" height="160" viewBox="0 0 160 160">
        <circle cx="80" cy="80" r="65" fill="none" stroke="#1e3a4a" stroke-width="12"/>
        <circle cx="80" cy="80" r="65" fill="none" stroke="{score_color}"
          stroke-width="12" stroke-linecap="round"
          stroke-dasharray="{2*3.14159*65}" stroke-dashoffset="{2*3.14159*65*(1-score/100)}"
          style="filter:drop-shadow(0 0 8px {score_color})"/>
      </svg>
      <div class="val">
        <span class="num">{score}</span>
        <span class="lbl">SECURITY</span>
      </div>
    </div>
  </div>

  <div class="grid2">
    <div class="card">
      <h2>◈ Target Profile</h2>
      <table>
        <tr><td>Domain</td><td>{intel.domain}</td></tr>
        <tr><td>IP Address</td><td>{intel.ip}</td></tr>
        <tr><td>ASN</td><td>{intel.asn}</td></tr>
        <tr><td>Organisation</td><td>{intel.org}</td></tr>
        <tr><td>Location</td><td>{intel.city}, {intel.country}</td></tr>
        <tr><td>Server</td><td>{intel.server}</td></tr>
        <tr><td>Status</td><td><span class="badge badge-{'g' if intel.status_code==200 else 'r'}">{intel.status_code}</span></td></tr>
        <tr><td>HTTP Version</td><td>{intel.http_version}</td></tr>
        <tr><td>Latency</td><td>{intel.latency_ms} ms</td></tr>
        <tr><td>CMS</td><td>{intel.cms}</td></tr>
        <tr><td>WAF</td><td>{'<span class="badge badge-g">'+intel.waf_detected+'</span>' if intel.waf_detected else '<span class="badge badge-r">NONE</span>'}</td></tr>
        <tr><td>CDN</td><td>{'<span class="badge badge-b">'+intel.cdn_detected+'</span>' if intel.cdn_detected else '—'}</td></tr>
      </table>
    </div>
    <div class="card">
      <h2>◈ SSL / TLS</h2>
      <table>
        <tr><td>Issuer</td><td>{intel.ssl_issuer}</td></tr>
        <tr><td>Expires</td><td>{intel.ssl_expiry}</td></tr>
        <tr><td>TLS Version</td><td>{intel.tls_version}</td></tr>
        <tr><td>Grade</td><td><span class="badge {'badge-g' if intel.ssl_grade=='A+' else 'badge-y' if intel.ssl_grade=='B' else 'badge-r'}">{intel.ssl_grade}</span></td></tr>
      </table>
    </div>
  </div>

  <div class="card" style="margin-bottom:20px">
    <h2>◈ Security Headers Analysis</h2>
    <table>
      <tr><th>Header</th><th>Value / Status</th></tr>
      {sec_rows or "<tr><td colspan='2'>No data</td></tr>"}
    </table>
  </div>

  <div class="grid2">
    <div class="card">
      <h2>◈ Open Ports</h2>
      <table>
        <tr><th>Port</th><th>Service</th><th>Banner</th></tr>
        {port_rows}
      </table>
    </div>
    <div class="card">
      <h2>◈ Forms Detected</h2>
      <table>
        <tr><th>Action</th><th>Method</th><th>Inputs</th></tr>
        {form_rows}
      </table>
    </div>
  </div>

  <div class="grid3">
    <div class="card">
      <h2>◈ Subdomains</h2>
      <ul>{subdomain_items}</ul>
    </div>
    <div class="card">
      <h2>◈ Emails Found</h2>
      <ul>{email_items}</ul>
    </div>
    <div class="card">
      <h2>◈ Technologies</h2>
      <ul>{tech_items}</ul>
    </div>
  </div>

  <div class="card" style="margin-bottom:20px">
    <h2>◈ Archive Statistics</h2>
    <table>
      <tr><td>Mode</td><td>{session.mode}</td></tr>
      <tr><td>Files Downloaded</td><td>{session.files_count}</td></tr>
      <tr><td>Total Size</td><td>{U.size(session.bytes_downloaded)}</td></tr>
      <tr><td>Duration</td><td>{int(session.elapsed)}s</td></tr>
      <tr><td>Avg Speed</td><td>{U.size(int(session.avg_speed))}/s</td></tr>
      <tr><td>Errors</td><td><span class="badge {'badge-r' if session.errors else 'badge-g'}">{len(session.errors)}</span></td></tr>
      <tr><td>Output Directory</td><td><code>{session.output_dir}</code></td></tr>
    </table>
  </div>

  <footer>TITAN OMEGA v8.0 NEXUS CORE — SOVEREIGN 2026 — REPORT ID: {U.uid("RPT")}</footer>
</div>
</body>
</html>"""
        out.write_text(html_content, encoding="utf-8")
        return out

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TERMINAL UI — 2026 REDESIGN
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BANNER = r"""[bold #FF00FF]
  _   _ _______  ___    _  _____   _____ ____  _____  ______
 | \ | |  ___\ \/ / |  | |/ ____| / ____/ __ \|  __ \|  ____|
 |  \| | |__  \  /| |  | | (___  | |   | |  | | |__) | |__
 | . ` |  __| /  \| |  | |\___ \ | |   | |  | |  _  /|  __|
 | |\  | |___/ /\ \ |__| |____) || |___| |__| | | \ \| |____
 |_| \_|______/_/ \_\____/|_____/  \____\____/|_|  \_\______|

[/][bold #00FFFF]          v8.0 SOVEREIGN EDITION (2026) [/]
"""

def _make_banner_panel():
    return Panel(
        Align.center(Text.from_markup(BANNER)),
        border_style="cyan",
        box=box.DOUBLE_EDGE,
    )

def _make_menu_table() -> Table:
    t = Table(
        box=box.SIMPLE_HEAD,
        header_style="bold cyan",
        show_edge=True,
        border_style="dim cyan",
        expand=True,
        pad_edge=True,
    )
    t.add_column("KEY",   justify="center", style="bold yellow",  width=5)
    t.add_column("MODULE",                  style="bold white",   width=22)
    t.add_column("DESCRIPTION",             style="dim",          ratio=2)
    t.add_column("FEATURES",                style="cyan",         ratio=2)

    rows = [
        ("1", "⬡ RECON — FAST",      "Quick 5-module reconnaissance",            "DNS · GeoIP · HTTP · SSL · Headers · WAF"),
        ("2", "⬡ RECON — DEEP",      "Full passive OSINT sweep",                  "+ Subdomains · Ports · Forms · Comments · Emails"),
        ("3", "⬡ DOWNLOAD SINGLE",   "Fetch single resource with hash check",     "Stealth UA · Redirect trace · SHA-256"),
        ("4", "⬡ SMART CRAWL",       "Async crawl depth-2 (15 concurrent)",       "Link extract · Asset save · Stats"),
        ("5", "⬡ DEEP CRAWL",        "Async crawl depth-4 (20 concurrent)",       "Full tree · JS · Media · Documents"),
        ("6", "⬡ FULL MIRROR",       "Site clone depth-6 (30 concurrent)",        "Complete offline copy · Index preserved"),
        ("7", "⬡ SITEMAP BLAST",     "Sitemap-driven bulk download",              "Auto-parse sitemap.xml · Parallel fetch"),
        ("8", "⬡ GENERATE REPORT",   "Export full HTML intelligence report",      "Security score · Ports · OSINT · Dark theme"),
        ("9", "⬡ VIEW ARCHIVES",     "Browse local archives tree",                "File browser · Size stats · Hash"),
        ("P", "⬡ LOAD PROXIES",      "Load proxy list (file or manual)",          "HTTP · HTTPS · SOCKS4 · SOCKS5 · Auth"),
        ("F", "⬡ FETCH FREE PROXIES", "Auto-download proxies from public lists",   "6 sources · health-check · rank by speed"),
        ("B", "⬡ BYPASS STATUS",     "AI brain + bypass stats per domain",        "Strategy · Success rate · Cookie jar"),
        ("Q", "⬡ EXIT",              "Shutdown with cleanup",                     "Temp purge · Log flush"),
    ]
    for k, m, d, f in rows:
        t.add_row(k, m, d, f)
    return t

def _make_live_layout(intel: TargetIntel, session: ArchiveSession, pulse: SystemPulse, engine: DownloadEngine) -> Layout:
    sys_data = pulse.sample()
    layout   = Layout()
    layout.split(
        Layout(name="hdr",  size=4),
        Layout(name="body", ratio=1),
        Layout(name="foot", size=3),
    )
    layout["body"].split_row(
        Layout(name="left",   ratio=1),
        Layout(name="center", ratio=2),
        Layout(name="right",  ratio=1),
    )

    # ── Header bar ───────────────────────────────────────────────────────────
    hdr_grid = Table.grid(expand=True)
    hdr_grid.add_column(justify="left",   style="bold cyan")
    hdr_grid.add_column(justify="center", style="bold white")
    hdr_grid.add_column(justify="right",  style="bold yellow")
    hdr_grid.add_row(
        f"[bold]NEXUS v8.0[/] ◈ {session.session_id}",
        f"⬡ {intel.domain} ◈ {session.mode}",
        f"⬡ {U.ts()} ◈ {session.status}",
    )
    layout["hdr"].update(Panel(hdr_grid, style="on grey7", box=box.HORIZONTALS))

    # ── Left — Intel ─────────────────────────────────────────────────────────
    it = Table.grid(padding=(0,1))
    it.add_column(style="bold cyan", min_width=10)
    it.add_column()
    rows_l = [
        ("IP",       intel.ip),
        ("ASN",      intel.asn[:25]),
        ("Location", f"{intel.city}, {intel.country}"),
        ("Server",   intel.server[:22]),
        ("CMS",      intel.cms),
        ("WAF",      intel.waf_detected or "—"),
        ("CDN",      intel.cdn_detected or "—"),
        ("Latency",  f"{intel.latency_ms}ms"),
        ("TLS",      intel.tls_version),
        ("SSL Grade",intel.ssl_grade),
        ("Score",    f"{intel.score}/100"),
    ]
    for k,v in rows_l:
        it.add_row(f"[cyan]{k}[/]", str(v)[:25])
    layout["left"].update(Panel(it, title="◈ INTEL", border_style="cyan"))

    # ── Center — Activity ────────────────────────────────────────────────────
    status_color = "[green]" if session.status == "RUNNING" else "[yellow]" if session.status == "INIT" else "[red]"
    status_msg = session.status

    # Calculate fake dynamic sparkline for speed
    val = min(100, int((intel.bandwidth_usage / (1024 * 1024)) * 10)) # Assuming bandwidth_usage is bytes/sec
    bar = "█" * (val // 5) + "░" * (20 - (val // 5))

    # Center - Activity
    lines = [
        f"[#FF00FF]► 𝐓𝐀𝐑𝐆𝐄𝐓:[/]      [bold white]{intel.target_url}[/]",
        f"[#00FFFF]► 𝐌𝐎𝐃𝐄:[/]        [bold white]{session.mode}[/]",
        f"[#FF00FF]► 𝐒𝐓𝐀𝐓𝐔𝐒:[/]      {status_color}{status_msg}[/]",
        "",
        f"[bold #FF00FF]⚡ 𝐏𝐄𝐑𝐅𝐎𝐑𝐌𝐀𝐍𝐂𝐄[/]",
        f"  Speed:    [bold #00FFFF]{U.size(int(session.avg_speed))}/s[/]", # Use session.avg_speed
        f"  Chart:    [#00FFFF]{bar}[/]",
        f"  Workers:  [magenta]{session.active_workers}[/] / {session.concurrency}",
        f"  Requests: {session.requests_sent} [dim](Errors: {len(session.failed_urls)})[/]",
        "",
        f"[bold #00FFFF]💾 𝐒𝐓𝐎𝐑𝐀𝐆𝐄[/]",
        f"  Files:    [white]{session.files_count}[/]",
        f"  Data:     [white]{U.size(session.bytes_downloaded)}[/]",
        "",
        "[bold dim]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/]",
        "[bold #FF00FF]Recent downloads:[/]",
    ]
    recent = list(session.completed_urls)[-5:]
    for url in reversed(recent):
        fname = url.split("/")[-1][:55] or "index.html"
        lines.append(f"  [dim green]▶[/] {fname}")
    if session.errors:
        lines.append("")
        lines.append("[bold red]Last error:[/]")
        lines.append(f"  [dim red]{session.errors[-1][:70]}[/]")
    layout["center"].update(Panel(
        "\n".join(lines),
        title="◈ OPERATIONS",
        border_style="white",
    ))

    # ── Right — System + Bypass ───────────────────────────────────────────────
    layout["right"].split(
        Layout(name="intel", size=14),
        Layout(name="bypass", size=14)
    )

    # Right Top - Intel
    intel_text = Text.from_markup("\n")
    if intel:
        waf_name = intel.waf_detected if intel.waf_detected else "[dim]None[/]"
        cms_disp = intel.cms if intel.cms else "[dim]Unknown[/]"
        intel_text.append_text(Text.from_markup(
            f"  [#FF00FF]WAF/CDN:[/]   [bold white]{waf_name}[/]\n"
            f"  [#00FFFF]CMS/Stack:[/] {cms_disp}\n\n"
            "  [bold dim]Tech Stack:[/]"
        ))
        for t in intel.technologies[:4]:
            intel_text.append_text(Text.from_markup(f"\n  [dim]•[/] {t}"))

        layout["intel"].update(Panel(intel_text, title="[#00FFFF]Target Intelligence[/]", border_style="#00FFFF"))
    else:
        layout["intel"].update(Panel("\n[dim]No intellect data gathered yet...[/]", title="[#00FFFF]Target Intelligence[/]", border_style="#00FFFF"))

    # Right Bottom - Bypass Status
    b_text = Text.from_markup("\n")
    if BYPASS._domain_states:
        # Just grab the state of the target domain
        dst = BYPASS._domain_states.get(urlparse(intel.target_url).netloc)
        active_proxies = sum(1 for p in BYPASS._proxy_records.values() if p.alive) # Corrected from p.status
        b_text.append_text(Text.from_markup(f"[#FF00FF]Global Proxy Pool:[/] {active_proxies} alive\n\n"))

        if dst:
            b_text.append_text(Text.from_markup(f"[#00FFFF]Active Target:[/] [white]{dst.domain}[/]\n"))
            b_text.append_text(Text.from_markup(f"  [dim]➔[/] Cookie Jar:  {len(dst.cookies)} stored\n"))
            b_text.append_text(Text.from_markup(f"  [dim]➔[/] CAPTCHA HIT: {dst.challenge_count} triggers\n"))
            # Visual marker for extreme curl_cffi use
            if dst.strategy in ("SPOOF", "PROXY", "ROTATE"):
                try:
                    import curl_cffi
                    b_text.append_text(Text.from_markup(f"  [dim]➔[/] Engine:      [bold #00FFFF]cURL_CFFI (JA3 Emulation)[/]\n"))
                except ImportError:
                    pass

    layout["bypass"].update(Panel(b_text, title="[#FF00FF]Nexus Bypass Engine[/]", border_style="#FF00FF"))

    # ── Footer ───────────────────────────────────────────────────────────────
    layout["foot"].update(Panel(
        Align.center(
            f"[bold]OUTPUT:[/] {session.output_dir}  ◈  [bold]CTRL+C[/] ABORT  ◈  [dim]NEXUS CORE 2026[/]"
        ),
        style="on grey7",
        box=box.HORIZONTALS,
    ))
    return layout

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MAIN ASYNC LOOP
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def main_loop():
    pulse          = SystemPulse()
    last_intel     = None
    last_session   = None

    while True:
        console.clear()
        console.print(_make_banner_panel())
        console.print()
        console.print(_make_menu_table())
        console.print()

        cmd = Prompt.ask(
            "[bold cyan]NEXUS ▶[/]",
            choices=["1","2","3","4","5","6","7","8","9","p","P","f","F","b","B","q","Q"],
            default="1",
        )

        # ── EXIT ─────────────────────────────────────────────────────────────
        if cmd.lower() == "q":
            console.print(Rule("[bold red]NEXUS SHUTDOWN[/]"))
            with console.status("[yellow]Purging temp files and cache…"):
                shutil.rmtree(TMP, ignore_errors=True)
                TMP.mkdir(exist_ok=True)
                shutil.rmtree(CACHE, ignore_errors=True)
                CACHE.mkdir(exist_ok=True)
            console.print("[green]✓ System clean. Goodbye.[/]\n")
            break

        # ── LOAD PROXIES ──────────────────────────────────────────────────────
        if cmd.lower() == "p":
            console.print(Rule("[bold yellow]◈ PROXY LOADER[/]"))
            console.print("[dim]Format: one proxy per line — http://ip:port or socks5://ip:port[/]")
            console.print("[dim]Leave blank to enter proxies manually, or type a file path.[/]\n")
            proxy_input = Prompt.ask("[cyan]Proxy file path or manual list (comma-separated)[/]", default="")
            if proxy_input.strip():
                if Path(proxy_input.strip()).exists():
                    BYPASS.load_proxies_from_file(proxy_input.strip())
                else:
                    proxies = [p.strip() for p in proxy_input.split(",") if p.strip()]
                    BYPASS.load_proxies(proxies)
            console.print(f"\n[green]✓ Proxy pool: {len(BYPASS._proxy_list)} proxies loaded[/]")
            if BYPASS._proxy_list:
                for px in BYPASS._proxy_list[:5]:
                    console.print(f"  [dim cyan]→ {px}[/]")
                if len(BYPASS._proxy_list) > 5:
                    console.print(f"  [dim]… and {len(BYPASS._proxy_list)-5} more[/]")
            input("\nPress Enter…")
            continue

        # ── FETCH FREE PROXIES ────────────────────────────────────────────────
        if cmd.lower() == "f":
            console.print(Rule("[bold yellow]◈ FETCH FREE PROXIES[/]"))
            with console.status("[yellow]Fetching from public APIs...[/]"):
                found = await BYPASS.fetch_free_proxies()
                await BYPASS.health_check_proxies()
            console.print(f"\n[bold green]✓ Proxy harvest complete: {found} found[/]")
            input("\nPress Enter…")
            continue

        # ── BYPASS STATUS ─────────────────────────────────────────────────────
        if cmd.lower() == "b":
            console.print(Rule("[bold cyan]◈ BYPASS ENGINE STATUS[/]"))
            bt = Table(box=box.ROUNDED, show_header=False, border_style="cyan")
            bt.add_column("K", style="bold cyan", min_width=22)
            bt.add_column("V")
            domains_with_cookies = sum(1 for d in BYPASS._domain_states.values() if d.cookies)
            bt.add_row("Total Requests",       str(BYPASS._req_count))
            bt.add_row("Proxy Pool",           f"{len(BYPASS._proxy_list)} proxies")
            bt.add_row("Alive Proxies",        str(sum(1 for r in BYPASS._proxy_records.values() if r.alive)))
            bt.add_row("Domains w/ Cookies",   str(domains_with_cookies))
            bt.add_row("Known Referers",       str(sum(1 for d in BYPASS._domain_states.values() if d.referer)))
            bt.add_row("UA Pool Size",         str(len(UA_POOL)))
            console.print(bt)
            console.print()
            # Show stored WAF cookies per domain
            if domains_with_cookies > 0:
                console.print("[bold yellow]Stored WAF Cookies:[/]")
                for domain, state in BYPASS._domain_states.items():
                    if state.cookies:
                        console.print(f"  [cyan]{domain}[/]")
                        for name, val in list(state.cookies.items())[:5]:
                            console.print(f"    [dim]{name}[/] = [green]{val[:30]}…[/]")
            else:
                console.print("[dim]No WAF cookies stored yet.[/]")
            input("\nPress Enter…")
            continue

        # ── REPORT ───────────────────────────────────────────────────────────
        if cmd == "8":
            if last_intel and last_session:
                with console.status("[yellow]Generating HTML report…"):
                    path = ReportGen.html(last_intel, last_session)
                console.print(f"\n[bold green]✓ Report saved:[/] {path}")
            else:
                console.print("[yellow]⚠ Run a recon or download first.[/]")
            input("\nPress Enter…")
            continue

        # ── VIEW ARCHIVES ─────────────────────────────────────────────────────
        if cmd == "9":
            archives = sorted(ARCH.glob("*"))
            if not archives:
                console.print("[yellow]No archives yet.[/]")
                input("\nPress Enter…")
                continue
            tree = Tree(f"[bold cyan]◈ NEXUS_ARCHIVES[/] ({len(archives)} sessions)")
            for arch in archives:
                files = list(arch.rglob("*"))
                total = sum(f.stat().st_size for f in files if f.is_file())
                branch = tree.add(f"[bold]{arch.name}[/] [dim]({U.size(total)}, {len([f for f in files if f.is_file()])} files)[/]")
                for f in sorted(files)[:12]:
                    if f.is_file():
                        branch.add(f"[dim]📄 {f.name} ({U.size(f.stat().st_size)})[/]")
            console.print(tree)
            input("\nPress Enter…")
            continue

        # ── ALL OPERATIONS NEED A TARGET ─────────────────────────────────────
        target = U.clean_url(Prompt.ask("\n[bold cyan]◈ Target URL[/]", default="example.com"))
        deep   = cmd == "2"

        # Recon phase
        console.print()
        recon  = ReconEngine(target)
        with console.status(f"[bold yellow]◈ Scanning {recon.domain}{'  [deep mode]' if deep else ''}…"):
            intel = await recon.run(deep=deep)
        last_intel = intel

        # Display recon results
        if cmd in ("1","2"):
            console.print(Rule("[bold cyan]◈ RECON RESULTS[/]"))

            prof = Table(box=box.ROUNDED, show_header=False, border_style="cyan")
            prof.add_column("K", style="bold cyan", min_width=18)
            prof.add_column("V")
            for k,v in [
                ("Domain",       intel.domain),
                ("IP / ASN",     f"{intel.ip}  {intel.asn}"),
                ("Org",          intel.org),
                ("Location",     f"{intel.city}, {intel.country}"),
                ("Server",       intel.server),
                ("HTTP Status",  str(intel.status_code)),
                ("Latency",      f"{intel.latency_ms} ms"),
                ("TLS",          intel.tls_version),
                ("SSL Grade",    intel.ssl_grade),
                ("SSL Issuer",   intel.ssl_issuer),
                ("SSL Expiry",   intel.ssl_expiry),
                ("CMS",          intel.cms),
                ("WAF",          intel.waf_detected or "None detected"),
                ("CDN",          intel.cdn_detected or "None"),
                ("Security Score",f"{intel.score}/100"),
            ]:
                prof.add_row(k, str(v))
            console.print(prof)

            if intel.security_headers or intel.missing_sec_headers:
                sh_t = Table(title="Security Headers", box=box.SIMPLE_HEAD, border_style="green")
                sh_t.add_column("Header"); sh_t.add_column("Status"); sh_t.add_column("Value")
                for h,v in intel.security_headers.items():
                    sh_t.add_row(h, "[green]✔ PRESENT[/]", v[:60])
                for h in intel.missing_sec_headers:
                    sh_t.add_row(h, "[red]✘ MISSING[/]", "—")
                console.print(sh_t)

            if deep:
                if intel.open_ports:
                    pt = Table(title="Open Ports", box=box.SIMPLE_HEAD, border_style="yellow")
                    pt.add_column("Port"); pt.add_column("Service"); pt.add_column("Banner")
                    for port,svc,banner in intel.open_ports:
                        pt.add_row(str(port), svc, banner or "—")
                    console.print(pt)
                if intel.subdomains:
                    console.print(Panel("\n".join(intel.subdomains[:20]), title="Subdomains", border_style="magenta"))
                if intel.emails:
                    console.print(Panel("  ".join(intel.emails), title="Emails Found", border_style="cyan"))
                if intel.forms:
                    console.print(f"[cyan]Forms:[/] {len(intel.forms)} found")
                if intel.comments:
                    console.print(Panel("\n".join(intel.comments[:5]), title="HTML Comments", border_style="yellow"))

            input("\n[dim]Press Enter to continue…[/]")
            continue

        # ── DOWNLOAD OPERATIONS ───────────────────────────────────────────────
        mode_map = {"3":"SINGLE","4":"CRAWL","5":"DEEP","6":"MIRROR","7":"SITEMAP"}
        mode = mode_map.get(cmd)
        if not mode:
            continue

        if not Confirm.ask(f"\n[yellow]Start {mode} archival on {recon.domain}?[/]", default=True):
            continue

        engine = DownloadEngine(target, mode, intel)
        last_session = engine.session
        engine_task  = asyncio.create_task(engine.run())

        console.print(f"\n[bold green]◈ {mode} initiated — Session {engine.session.session_id}[/]\n")

        try:
            with Live(
                _make_live_layout(intel, engine.session, pulse, engine),
                refresh_per_second=3,
                screen=False,
                transient=False,
            ) as live:
                while not engine_task.done():
                    live.update(_make_live_layout(intel, engine.session, pulse, engine))
                    await asyncio.sleep(0.4)
            await engine_task
        except KeyboardInterrupt:
            console.print("\n[bold red]⚠ Aborted by user.[/]")
            engine._stop = True

        # Summary
        s = engine.session
        console.print(Rule("[bold green]◈ MISSION COMPLETE[/]"))
        sum_t = Table(box=box.ROUNDED, show_header=False, border_style="green")
        sum_t.add_column("K", style="bold cyan", min_width=16)
        sum_t.add_column("V")
        sum_t.add_row("Session ID",     s.session_id)
        sum_t.add_row("Mode",           s.mode)
        sum_t.add_row("Files",          str(s.files_count))
        sum_t.add_row("Total Size",     U.size(s.bytes_downloaded))
        sum_t.add_row("Duration",       f"{int(s.elapsed)}s")
        sum_t.add_row("Avg Speed",      U.size(int(s.avg_speed)) + "/s")
        sum_t.add_row("Errors",         str(len(s.errors)))
        sum_t.add_row("Output",         str(s.output_dir))
        console.print(sum_t)

        if Confirm.ask("\n[cyan]Generate HTML report now?[/]", default=True):
            with console.status("[yellow]Building report…"):
                rp = ReportGen.html(intel, s)
            console.print(f"[green]✓ Report:[/] {rp}")

        input("\n[dim]Press Enter…[/]")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ENTRY POINT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        console.print("\n[bold red]Emergency shutdown.[/]")
    except Exception as e:
        log.critical(f"FATAL: {e}", exc_info=True)
        console.print_exception()
    finally:
        console.print("[dim]NEXUS CORE terminated.[/]")

if __name__ == "__main__":
    main()
