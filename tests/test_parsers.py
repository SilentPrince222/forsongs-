import pytest
from unittest.mock import AsyncMock
from src.infrastructure.sources.fma_parser import FMAMusicParser
from src.infrastructure.sources.jamendo_parser import JamendoMusicParser

@pytest.fixture
def mock_http_client():
    client = AsyncMock()
    return client

@pytest.mark.asyncio
async def test_fma_parser_search(mock_http_client):
    mock_http_client.get.return_value = {
        "data": [
            {
                "track_id": "123",
                "track_title": "Test Song",
                "artist_name": "Test Artist",
                "track_duration": "3:00",
                "track_url": "123-url",
                "track_license": "creative commons",
                "track_mp3": "http://example.com/download/123"
            }
        ]
    }
    
    parser = FMAMusicParser(mock_http_client)
    results = await parser.search("test", limit=1)
    
    assert len(results) == 1
    track = results[0]
    assert track.title == "Test Song"
    assert track.artist == "Test Artist"
    assert track.source == "fma"
    assert track.download_url == "http://example.com/download/123"

@pytest.mark.asyncio
async def test_fma_parser_download_url(mock_http_client):
    mock_http_client.get.return_value = {
        "data": [
            {
                "track_mp3": "http://example.com/download/123"
            }
        ]
    }
    parser = FMAMusicParser(mock_http_client)
    url = await parser.get_download_url("123")
    assert url == "http://example.com/download/123"

@pytest.mark.asyncio
async def test_jamendo_parser_search(mock_http_client):
    mock_http_client.get.return_value = {
        "results": [
            {
                "id": "456",
                "name": "Jamendo Song",
                "artist_name": "Jamendo Artist",
                "duration": 180,
                "shareurl": "http://jamendo.com/456",
                "audiodownload": "http://jamendo.com/download/456",
                "image": "http://jamendo.com/cover/456"
            }
        ]
    }
    
    parser = JamendoMusicParser(mock_http_client)
    results = await parser.search("jamendo", limit=1)
    
    assert len(results) == 1
    track = results[0]
    assert track.title == "Jamendo Song"
    assert track.artist == "Jamendo Artist"
    assert track.source == "jamendo"

@pytest.mark.asyncio
async def test_jamendo_parser_download_url(mock_http_client):
    mock_http_client.get.return_value = {
        "results": [
            {
                "audiodownload": "http://jamendo.com/download/456"
            }
        ]
    }
    parser = JamendoMusicParser(mock_http_client)
    url = await parser.get_download_url("456")
    assert url == "http://jamendo.com/download/456"