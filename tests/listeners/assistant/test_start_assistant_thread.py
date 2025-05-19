"""
Tests for the start_assistant_thread handler.
"""
import logging
from unittest.mock import Mock

from slack_bolt import Say, SetSuggestedPrompts

from listeners.assistant.start_assistant_thread import start_assistant_thread

test_logger = logging.getLogger(__name__)


class TestStartAssistantThread:
    """Tests for the start_assistant_thread handler."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.fake_say = Mock(Say)
        self.fake_set_suggested_prompts = Mock(SetSuggestedPrompts)
    
    def test_start_assistant_thread_success(self):
        """Test that the handler sends a welcome message and sets suggested prompts."""
        # Call the handler
        start_assistant_thread(
            say=self.fake_say,
            set_suggested_prompts=self.fake_set_suggested_prompts,
            logger=test_logger,
        )
        
        # Verify that say was called with the welcome message
        self.fake_say.assert_called_once()
        assert "How can I help you" in self.fake_say.call_args.args[0]
        
        # Verify that set_suggested_prompts was called with the expected prompts
        self.fake_set_suggested_prompts.assert_called_once()
        kwargs = self.fake_set_suggested_prompts.call_args.kwargs
        assert "prompts" in kwargs
        assert len(kwargs["prompts"]) > 0
        assert "title" in kwargs["prompts"][0]
        assert "message" in kwargs["prompts"][0]
    
    def test_say_exception(self, caplog):
        """Test that exceptions in the say function are properly handled."""
        # Set up the mock to raise an exception
        self.fake_say.side_effect = Exception("test exception")
        
        # Call the handler - this will raise an exception but we expect it to be caught
        # and logged in the handler
        try:
            start_assistant_thread(
                say=self.fake_say,
                set_suggested_prompts=self.fake_set_suggested_prompts,
                logger=test_logger,
            )
        except Exception:
            # The exception is expected to propagate in the test environment
            pass
        
        # Verify that the exception was logged
        assert "test exception" in caplog.text
    
    def test_set_suggested_prompts_exception(self, caplog):
        """Test that exceptions in the set_suggested_prompts function are properly handled."""
        # Set up the mock to raise an exception
        self.fake_set_suggested_prompts.side_effect = Exception("test exception")
        
        # Call the handler
        start_assistant_thread(
            say=self.fake_say,
            set_suggested_prompts=self.fake_set_suggested_prompts,
            logger=test_logger,
        )
        
        # Verify that the exception was logged
        assert "test exception" in caplog.text
        
        # Verify that say was called with the error message
        assert self.fake_say.call_count == 2
        error_call = self.fake_say.call_args_list[1]
        assert "Error" in error_call.args[0]
