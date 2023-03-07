from abc import ABC, abstractmethod


class BaseServiceEmail(ABC):
    """Email sending service."""

    @abstractmethod
    def send_email(self, to_email: str, subject: str, content: str) -> bool:
        """Send email. Return true when a successful result."""
        pass
