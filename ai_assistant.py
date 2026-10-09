import json
import requests
from typing import Generator, List, Dict, Any, Tuple

GROQ_CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODELS_URL = "https://api.groq.com/openai/v1/models"

DEFAULT_MODELS = [
    "qwen/qwen3.8-27b",
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "allam-2-7b"
]

def get_available_models(api_key: str) -> List[str]:
    """Fetches available models from Groq API or falls back to known defaults."""
    if not api_key:
        return DEFAULT_MODELS
    try:
        res = requests.get(
            GROQ_MODELS_URL,
            headers={"Authorization": f"Bearer {api_key.strip()}"},
            timeout=5
        )
        if res.status_code == 200:
            data = res.json()
            models = [
                m["id"] for m in data.get("data", [])
                if not m["id"].startswith("whisper") and "guard" not in m["id"].lower()
            ]
            if models:
                preferred = ["qwen/qwen3.8-27b", "openai/gpt-oss-120b", "openai/gpt-oss-20b"]
                sorted_models = [m for m in preferred if m in models] + [m for m in models if m not in preferred]
                return sorted_models
    except Exception:
        pass
    return DEFAULT_MODELS

def stream_groq_chat(
    api_key: str,
    messages: List[Dict[str, str]],
    model: str = "qwen/qwen3.8-27b",
    temperature: float = 0.7,
    max_tokens: int = 2048
) -> Generator[str, None, None]:
    """Streams chat tokens from the Groq OpenAI-compatible completions endpoint."""
    if not api_key or not api_key.strip():
        raise ValueError("No Groq API key provided. Please configure it in the settings.")

    headers = {
        "Authorization": f"Bearer {api_key.strip()}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": True
    }

    try:
        response = requests.post(
            GROQ_CHAT_URL,
            headers=headers,
            json=payload,
            stream=True,
            timeout=30
        )
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Connection to Groq API failed: {e}")

    if response.status_code != 200:
        try:
            err_msg = response.json().get("error", {}).get("message", response.text)
        except Exception:
            err_msg = response.text
        raise RuntimeError(f"Groq API Error ({response.status_code}): {err_msg}")

    for line in response.iter_lines():
        if not line:
            continue
        decoded = line.decode("utf-8")
        if decoded.startswith("data: "):
            chunk_data = decoded[6:].strip()
            if chunk_data == "[DONE]":
                break
            try:
                chunk_json = json.loads(chunk_data)
                delta = chunk_json.get("choices", [{}])[0].get("delta", {})
                content = delta.get("content")
                if content:
                    yield content
            except json.JSONDecodeError:
                continue

def send_groq_chat(
    api_key: str,
    messages: List[Dict[str, str]],
    model: str = "qwen/qwen3.8-27b",
    temperature: float = 0.7,
    max_tokens: int = 2048
) -> str:
    """Non-streaming fallback to obtain a direct chat completion response."""
    if not api_key or not api_key.strip():
        raise ValueError("No Groq API key provided.")

    headers = {
        "Authorization": f"Bearer {api_key.strip()}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False
    }

    response = requests.post(
        GROQ_CHAT_URL,
        headers=headers,
        json=payload,
        timeout=30
    )

    if response.status_code != 200:
        try:
            err_msg = response.json().get("error", {}).get("message", response.text)
        except Exception:
            err_msg = response.text
        raise RuntimeError(f"Groq API Error ({response.status_code}): {err_msg}")

    data = response.json()
    return data["choices"][0]["message"]["content"]

def build_system_prompt(hunter: Dict[str, Any], cfg: Dict[str, Any], style: str = "System Monarch Companion") -> str:
    """Builds a rich, context-aware system prompt tailored to Arpit's Solo Leveling tracker."""
    name = cfg.get("hunter_name", "Arpit")
    title = cfg.get("hunter_title", "Shadow Monarch in Training")
    level = hunter.get("level", 1)
    rank = hunter.get("rank", "E-Rank")
    tier = hunter.get("tier", "Novice Hunter")
    total_xp = hunter.get("total_xp", 0)
    streak = hunter.get("streak", 0)
    day_num = hunter.get("day_num", 1)
    total_days = hunter.get("total_days", 92)

    base_context = (
        f"You are the embedded AI System for {name}, an awakened developer and engineering student.\n"
        f"CURRENT STATUS HUD:\n"
        f"- Player Name: {name}\n"
        f"- Title: {title}\n"
        f"- Level: LV. {level} ({rank} | {tier})\n"
        f"- Cumulative Output: {total_xp:,} EXP\n"
        f"- Winter Arc Sprint: Day {day_num} of {total_days} (Oct 1 → Dec 31, 2026)\n"
        f"- Lock-In Streak: {streak} Days\n\n"
        f"CORE STUDY & TECHNICAL CURRICULUM:\n"
        f"1. Semester 3 Academics: Mathematics III (Linear & Partial Differential Equations, Variation of Parameters, "
        f"Charpit's method, Vector Calculus, Green's, Gauss, and Stokes' Theorems), "
        f"Computer Organization & Operating Systems (COOS - memory hierarchy, pipelining, CPU scheduling, paging), "
        f"Data Structures & Algorithms (Java implementation, LeetCode patterns, trees, graphs, DP), "
        f"Python mastery, and Universal Human Values (UHV).\n"
        f"2. Agentic AI Roadmap (Phases 1–12): LangGraph stateful graphs, autonomous agents, tool orchestration, MCP, multi-agent swarms, self-reflection.\n"
        f"3. ML Project X-0 (Phase 0 100 Topics): Foundations from scratch (Scaled Dot-Product Attention, Multi-Head Attention, RoPE, KV cache, backward pass, CUDA).\n"
        f"4. Projects & Code: Python, Streamlit, PyTorch, LangChain, SQLite.\n"
    )

    if style == "System Monarch Companion":
        return (
            f"{base_context}\n"
            f"PERSONA: You speak as the omniscient, loyal, and motivating 'Solo Leveling System Interface' / 'Shadow Companion'. "
            f"You address {name} with respect as the Player. "
            f"You provide elite technical explanations, sharp mathematical derivations, clean code, and disciplined motivation to sustain peak focus during this Winter Arc sprint. "
            f"Keep explanations clear, structured with markdown, and mathematically/computationally accurate."
        )
    elif style == "Academic & Code Tutor":
        return (
            f"{base_context}\n"
            f"PERSONA: You are a distinguished Computer Science professor and Senior AI Research Engineer. "
            f"Provide rigorous, step-by-step mathematical proofs, solve differential equations clearly, "
            f"debug complex algorithms, and provide clean code with time and space complexity analysis."
        )
    else:
        return (
            f"{base_context}\n"
            f"PERSONA: You are an all-around AI engineering and study partner assisting {name} with questions, planning, and code."
        )
