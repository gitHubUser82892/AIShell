"""
Custom exceptions for the AICLI package
"""

class AICLIError(Exception):
    """Base exception for AICLI"""
    pass

class ConfigurationError(AICLIError):
    """Raised when there's a configuration issue"""
    pass

class APIError(AICLIError):
    """Raised when there's an API communication error"""
    pass

class CommandExecutionError(AICLIError):
    """Raised when command execution fails"""
    pass

class HistoryError(AICLIError):
    """Raised when there's an issue with command history"""
    pass 