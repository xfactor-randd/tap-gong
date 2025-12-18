"""Tests standard tap features using the built-in SDK tests library."""

import datetime

from tap_gong.tap import TapGong

SAMPLE_CONFIG = {
    "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "end_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "access_key": "foo",
    "access_key_secret": "bar",
}


def test_tap_instantiation():
    """Test that tap can be instantiated with valid config."""
    tap = TapGong(config=SAMPLE_CONFIG)
    assert tap.name == "tap-gong"
    assert tap.config == SAMPLE_CONFIG


def test_stream_discovery():
    """Test that streams can be discovered."""
    tap = TapGong(config=SAMPLE_CONFIG)
    streams = tap.discover_streams()

    # Should have 5 streams based on STREAM_TYPES in tap.py
    assert len(streams) == 5

    # Check that expected streams are present
    stream_names = [stream.name for stream in streams]
    expected_streams = [
        "calls",
        "call_transcripts",
        "users",
        "interaction_stats",
        "aggregated_activity"
    ]

    for expected_stream in expected_streams:
        assert expected_stream in stream_names


def test_config_validation():
    """Test config validation works correctly."""
    # Test missing required field
    invalid_config = {"access_key": "foo"}

    try:
        TapGong(config=invalid_config)
        assert False, "Should have raised ConfigValidationError"
    except Exception as e:
        assert "Config validation failed" in str(e)
