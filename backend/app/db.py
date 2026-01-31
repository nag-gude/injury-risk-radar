import json
import os
from typing import Any

from redis import Redis

_client = None


def get_client() -> Redis:
    global _client
    if _client is not None:
        return _client

    redis_url = os.getenv("KV_URL") or os.getenv("REDIS_URL")
    if not redis_url:
        raise RuntimeError("KV_URL or REDIS_URL is required for Vercel KV")

    _client = Redis.from_url(redis_url, decode_responses=True)
    return _client


def _user_key(user_id: str) -> str:
    return f"user:{user_id}"


def _user_email_key(email: str) -> str:
    return f"user_email:{email.lower()}"


def _log_key(log_id: str) -> str:
    return f"log:{log_id}"


def _log_date_key(user_id: str, log_date: str) -> str:
    return f"log_date:{user_id}:{log_date}"


def _user_logs_key(user_id: str) -> str:
    return f"logs:{user_id}"


def create_user(user_data: dict) -> dict | None:
    client = get_client()
    email_key = _user_email_key(user_data["email"])
    if client.exists(email_key):
        return None

    client.set(email_key, user_data["id"])
    client.set(_user_key(user_data["id"]), json.dumps(user_data))
    return user_data


def get_user_by_email(email: str) -> dict | None:
    client = get_client()
    user_id = client.get(_user_email_key(email))
    if not user_id:
        return None
    return get_user_by_id(user_id)


def get_user_by_id(user_id: str) -> dict | None:
    client = get_client()
    payload = client.get(_user_key(user_id))
    if not payload:
        return None
    return json.loads(payload)


def get_log_by_date(user_id: str, log_date: str) -> dict | None:
    client = get_client()
    log_id = client.get(_log_date_key(user_id, log_date))
    if not log_id:
        return None
    return get_log_by_id(log_id)


def get_log_by_id(log_id: str) -> dict | None:
    client = get_client()
    payload = client.get(_log_key(log_id))
    if not payload:
        return None
    return json.loads(payload)


def create_log(log_data: dict) -> dict | None:
    client = get_client()
    log_date = log_data["log_date"]
    date_key = _log_date_key(log_data["user_id"], log_date)
    if client.exists(date_key):
        return None

    client.set(date_key, log_data["id"])
    client.rpush(_user_logs_key(log_data["user_id"]), log_data["id"])
    client.set(_log_key(log_data["id"]), json.dumps(log_data))
    return log_data


def list_logs(user_id: str) -> list[dict[str, Any]]:
    client = get_client()
    log_ids = client.lrange(_user_logs_key(user_id), 0, -1)
    logs: list[dict[str, Any]] = []
    for log_id in log_ids:
        payload = client.get(_log_key(log_id))
        if payload:
            logs.append(json.loads(payload))
    return logs
