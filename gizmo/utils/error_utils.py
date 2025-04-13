"""
Error utilities for Gizmo.

This module provides utility functions for error handling and recovery strategies.
"""

import asyncio
import functools
import logging
import threading
import time
from typing import Callable, Any, Optional, Type, Union, Tuple, TypeVar, Awaitable

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create a thread-local storage for step context
_step_context = threading.local()


class StepLoggerAdapter(logging.LoggerAdapter):
    """
    A logger adapter that adds step information to log messages.
    """
    def __init__(self, logger, extra=None):
        """
        Initialize the adapter with a logger and optional extra context.

        Args:
            logger (logging.Logger): The logger to adapt
            extra (dict, optional): Extra context to add to log messages
        """
        super().__init__(logger, extra or {})

    def process(self, msg, kwargs):
        """
        Process the log message to add step information if available.

        Args:
            msg (str): The log message
            kwargs (dict): Keyword arguments for the logging call

        Returns:
            tuple: The processed message and kwargs
        """
        # Check if we have step context
        step_num = getattr(_step_context, 'step_num', None)
        if step_num is not None:
            # Add step prefix to the message
            msg = f"[Step #{step_num}] {msg}"
        return msg, kwargs


def set_step_context(step_num):
    """
    Set the current step context for logging.

    Args:
        step_num (int): The current step number
    """
    _step_context.step_num = step_num


def clear_step_context():
    """
    Clear the current step context for logging.
    """
    if hasattr(_step_context, 'step_num'):
        delattr(_step_context, 'step_num')


# Create the base logger and wrap it with our adapter
base_logger = logging.getLogger('gizmo')
logger = StepLoggerAdapter(base_logger)


T = TypeVar('T')

def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: Union[Type[Exception], Tuple[Type[Exception], ...]] = Exception
) -> Callable:
    """
    Retry decorator for functions that might fail temporarily.
    Works with both synchronous and asynchronous functions.

    Args:
        max_attempts (int): Maximum number of attempts
        delay (float): Initial delay between attempts in seconds
        backoff_factor (float): Factor by which the delay increases with each attempt
        exceptions (Exception or tuple): Exceptions to catch and retry

    Returns:
        Callable: Decorated function
    """
    def decorator(func: Callable[..., Union[T, Awaitable[T]]]) -> Callable[..., Union[T, Awaitable[T]]]:
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs) -> T:
            current_delay = delay
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts:
                        logger.warning(
                            f"Attempt {attempt}/{max_attempts} for {func.__name__} failed: {str(e)}. "
                            f"Retrying in {current_delay:.2f} seconds..."
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff_factor
                    else:
                        logger.error(
                            f"All {max_attempts} attempts for {func.__name__} failed. "
                            f"Last error: {str(e)}"
                        )

            # If we get here, all attempts failed
            raise last_exception

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs) -> T:
            current_delay = delay
            last_exception = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts:
                        logger.warning(
                            f"Attempt {attempt}/{max_attempts} for {func.__name__} failed: {str(e)}. "
                            f"Retrying in {current_delay:.2f} seconds..."
                        )
                        await asyncio.sleep(current_delay)
                        current_delay *= backoff_factor
                    else:
                        logger.error(
                            f"All {max_attempts} attempts for {func.__name__} failed. "
                            f"Last error: {str(e)}"
                        )

            # If we get here, all attempts failed
            raise last_exception

        # Check if the function is a coroutine function
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


def safe_execute(
    func: Callable,
    *args,
    default_return: Any = None,
    error_message: str = "Operation failed",
    log_level: int = logging.ERROR,
    **kwargs
) -> Any:
    """
    Execute a function safely, catching any exceptions.

    Args:
        func (Callable): Function to execute
        *args: Arguments to pass to the function
        default_return (Any): Value to return if the function fails
        error_message (str): Message to log if the function fails
        log_level (int): Logging level for errors
        **kwargs: Keyword arguments to pass to the function

    Returns:
        Any: Result of the function or default_return if it fails
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.log(log_level, f"{error_message}: {str(e)}")
        return default_return


def log_error(
    error: Exception,
    message: str = "An error occurred",
    log_level: int = logging.ERROR
) -> None:
    """
    Log an error with a custom message.

    Args:
        error (Exception): The exception to log
        message (str): Custom message to prepend to the error
        log_level (int): Logging level for the error
    """
    logger.log(log_level, f"{message}: {str(error)}")


def handle_agent_error(
    agent_name: str,
    step_number: int,
    error: Exception,
    fallback_content: Optional[str] = None
) -> str:
    """
    Handle errors from agent execution.

    Args:
        agent_name (str): Name of the agent that failed
        step_number (int): Step number being processed
        error (Exception): The exception that occurred
        fallback_content (str, optional): Fallback content to return if available

    Returns:
        str: Error message or fallback content
    """
    error_message = f"Error in {agent_name} for step {step_number}: {str(error)}"
    logger.error(error_message)

    if fallback_content:
        logger.info(f"Using fallback content for {agent_name} in step {step_number}")
        return fallback_content

    return (
        f"# Error in {agent_name}\n\n"
        f"An error occurred while processing this step: {str(error)}\n\n"
        f"Please check the logs for more details."
    )
