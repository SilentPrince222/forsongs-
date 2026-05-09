import aiohttp
import asyncio
from typing import Optional, Callable, Any
from src.domain import HttpClient


class AioHttpClient(HttpClient):
    """aiohttp implementation of HttpClient."""

    def __init__(self, timeout: int = 30, user_agent: str = "Forsong/1.0"):
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.user_agent = user_agent
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession(
            timeout=self.timeout,
            headers={'User-Agent': self.user_agent}
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()

    async def get(self, url: str, **kwargs) -> dict:
        """Perform GET request."""
        if not self.session:
            raise RuntimeError("HttpClient must be used as async context manager")

        async with self.session.get(url, **kwargs) as response:
            if response.content_type == 'application/json':
                return await response.json()
            else:
                # For APIs that return JSON but don't set content-type properly
                text = await response.text()
                try:
                    import json
                    return json.loads(text)
                except json.JSONDecodeError:
                    return {'text': text, 'status': response.status}

    async def post(self, url: str, data: dict = None, **kwargs) -> dict:
        """Perform POST request."""
        if not self.session:
            raise RuntimeError("HttpClient must be used as async context manager")

        async with self.session.post(url, json=data, **kwargs) as response:
            return await response.json()

    async def download_file(self, url: str, output_path: str, progress_callback: Optional[Callable] = None) -> bool:
        """Download file with progress callback."""
        if not self.session:
            raise RuntimeError("HttpClient must be used as async context manager")

        try:
            async with self.session.get(url) as response:
                response.raise_for_status()

                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0

                with open(output_path, 'wb') as f:
                    async for chunk in response.content.iter_chunked(8192):
                        f.write(chunk)
                        downloaded += len(chunk)

                        if progress_callback and total_size > 0:
                            progress = downloaded / total_size
                            # For progress callback, we need to estimate speed and ETA
                            # This is simplified - real implementation would track timing
                            progress_callback(progress, 0, 0)

                return True

        except Exception as e:
            print(f"Download failed: {e}")
            return False