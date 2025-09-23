import httpx
import asyncio

async def buscar_archivo(peer_url: str, archivo: str, timeout=3):
    # peer_url ejemplo: http://127.0.0.1:8001
    url = f"{peer_url.rstrip('/')}/buscar?archivo={archivo}"
    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.get(url)
        r.raise_for_status()
        return r.json()
