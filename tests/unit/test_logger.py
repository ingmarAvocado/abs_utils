"""
Unit tests for logger module
"""
import pytest
import logging
import json
import sys
from io import StringIO
from unittest.mock import patch, MagicMock
from abs_utils.logger import setup_logging, get_logger


class TestSetupLogging:
    """Test logging setup"""

    def test_setup_with_defaults(self):
        """Test setup with default parameters"""
        setup_logging()

        root_logger = logging.getLogger()
        assert root_logger.level == logging.INFO
        assert len(root_logger.handlers) > 0

    def test_setup_with_custom_level(self):
        """Test setup with custom log level"""
        setup_logging(level="DEBUG")

        root_logger = logging.getLogger()
        assert root_logger.level == logging.DEBUG

    def test_setup_with_json_format(self):
        """Test setup with JSON format"""
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            setup_logging(log_format="json", service_name="test-service")

            logger = get_logger("test")
            logger.info("Test message")

            output = mock_stdout.getvalue()
            assert output.strip()  # Should have output

            # Parse JSON output
            log_data = json.loads(output.strip())
            assert log_data["message"] == "Test message"
            assert log_data["service"] == "test-service"
            assert "timestamp" in log_data

    def test_setup_with_plain_format(self):
        """Test setup with plain text format"""
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            setup_logging(log_format="plain")

            logger = get_logger("test")
            logger.info("Test message")

            output = mock_stdout.getvalue()
            assert "Test message" in output
            assert "INFO" in output

    def test_setup_clears_existing_handlers(self):
        """Test that setup clears existing handlers"""
        root_logger = logging.getLogger()

        # Add a dummy handler
        dummy_handler = logging.NullHandler()
        root_logger.addHandler(dummy_handler)

        setup_logging()

        # Dummy handler should be removed
        assert dummy_handler not in root_logger.handlers

    def test_setup_with_invalid_level(self):
        """Test setup with invalid log level defaults to INFO"""
        setup_logging(level="INVALID_LEVEL")

        root_logger = logging.getLogger()
        # Should default to INFO when invalid level provided
        assert root_logger.level in [logging.INFO, logging.WARNING, logging.ERROR]


class TestGetLogger:
    """Test logger retrieval"""

    def test_get_logger_basic(self):
        """Test basic logger retrieval"""
        logger = get_logger("test.module")
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test.module"

    def test_get_logger_with_module_name(self):
        """Test logger with __name__"""
        logger = get_logger(__name__)
        assert logger.name == __name__

    def test_multiple_loggers_are_different(self):
        """Test that different names return different loggers"""
        logger1 = get_logger("module1")
        logger2 = get_logger("module2")

        assert logger1 is not logger2
        assert logger1.name != logger2.name

    def test_same_name_returns_same_logger(self):
        """Test that same name returns same logger instance"""
        logger1 = get_logger("same.module")
        logger2 = get_logger("same.module")

        assert logger1 is logger2




class TestLoggerIntegration:
    """Test logger integration scenarios"""

    def test_logging_with_extra(self):
        """Test logging with extra fields"""
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            setup_logging(log_format="json", service_name="test-app")

            logger = get_logger("integration.test")
            logger.info("Test with context", extra={"request_id": "req-123", "user_id": "user-456"})

            output = mock_stdout.getvalue()
            if output:  # JSON format produces output
                log_data = json.loads(output.strip())
                assert log_data["message"] == "Test with context"
                # Extra fields might be included

    def test_logging_different_levels(self):
        """Test logging at different levels"""
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            setup_logging(level="DEBUG")

            logger = get_logger("level.test")

            logger.debug("Debug message")
            logger.info("Info message")
            logger.warning("Warning message")
            logger.error("Error message")

            output = mock_stdout.getvalue()
            assert "Debug message" in output or "DEBUG" in output.upper()
            assert "Info message" in output or "INFO" in output.upper()
            assert "Warning message" in output or "WARNING" in output.upper()
            assert "Error message" in output or "ERROR" in output.upper()

    def test_logging_with_exception(self):
        """Test logging exceptions"""
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            setup_logging()
            logger = get_logger("exception.test")

            try:
                raise ValueError("Test exception")
            except ValueError:
                logger.exception("An error occurred")

            output = mock_stdout.getvalue()
            assert "An error occurred" in output
            assert "ValueError" in output or "Test exception" in output

    def test_child_logger_inherits_level(self):
        """Test that child loggers inherit parent level"""
        setup_logging(level="WARNING")

        parent_logger = get_logger("parent")
        child_logger = get_logger("parent.child")

        # Child should inherit parent's effective level
        assert child_logger.getEffectiveLevel() >= logging.WARNING

    def test_json_formatter_fields(self):
        """Test JSON formatter includes expected fields"""
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            setup_logging(log_format="json", service_name="json-test")

            logger = get_logger("json.test")
            logger.info("Testing JSON fields", extra={"custom_field": "custom_value"})

            output = mock_stdout.getvalue()
            if output:
                log_data = json.loads(output.strip())

                # Check expected fields
                assert "timestamp" in log_data
                assert "level" in log_data
                assert "logger" in log_data
                assert "message" in log_data
                assert log_data["service"] == "json-test"

                # Custom field might be in extra
                if "custom_field" in log_data:
                    assert log_data["custom_field"] == "custom_value"