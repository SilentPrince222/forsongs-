import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from src.application.services.download_service import DownloadService

@pytest.fixture
def mock_track_repo():
    return AsyncMock()

@pytest.fixture
def mock_download_manager():
    return AsyncMock()

@pytest.mark.asyncio
async def test_download_service_initialization(mock_track_repo, mock_download_manager):
    service = DownloadService(
        track_repository=mock_track_repo,
        download_manager=mock_download_manager
    )
    assert service.track_repository == mock_track_repo
    assert service.download_manager == mock_download_manager
