"""
Script isolado para testar a extração de dados da API do HackerNews.
Ainda não está integrado ao Celery — isso fica para a Semana 2.

Como rodar (de dentro da pasta backend/):
    python -m workers.scraper
"""

import asyncio
from typing import Any

import httpx

HN_BASE_URL = "https://hacker-news.firebaseio.com/v0"
MAX_STORIES = 20


async def fetch_top_story_ids(client: httpx.AsyncClient) -> list[int]:
    response = await client.get(f"{HN_BASE_URL}/topstories.json")
    response.raise_for_status()
    return response.json()[:MAX_STORIES]


async def fetch_item(client: httpx.AsyncClient, item_id: int) -> dict[str, Any]:
    response = await client.get(f"{HN_BASE_URL}/item/{item_id}.json")
    response.raise_for_status()
    return response.json()


async def fetch_top_stories() -> list[dict[str, Any]]:
    async with httpx.AsyncClient(timeout=10.0) as client:
        story_ids = await fetch_top_story_ids(client)

        tasks = [
            fetch_item(client, story_id)
            for story_id in story_ids
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        return [
            story
            for story in results
            if isinstance(story, dict)
        ]


def main() -> None:
    stories = asyncio.run(fetch_top_stories())

    for story in stories:
        title = story.get("title", "(sem titulo)")
        url = story.get("url", "(sem url)")
        score = story.get("score", 0)

        print(f"[{score:>4}] {title}\n       {url}\n")


if __name__ == "__main__":
    main()