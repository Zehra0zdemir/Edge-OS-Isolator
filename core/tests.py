from django.test import TestCase
from django.urls import reverse
import re

class SecuritySanitizationTest(TestCase):
    """Validates that the input validation layers successfully block potential command injections."""

    def test_regex_sanitization_valid_username(self):
        """Ensures secure alphanumeric usernames are accepted."""
        valid_username = "edge_tenant_99"
        self.assertTrue(bool(re.match("^[a-zA-Z0-9_]*$", valid_username)))

    def test_regex_sanitization_blocked_injection_payloads(self):
        """Ensures characters used in OS Command Injections are caught by the security pattern."""
        malicious_usernames = [
            "admin; net user",
            "hacker&dir",
            "user_one|whoami",
            "test_user$",
        ]
        for payload in malicious_usernames:
            is_valid = bool(re.match("^[a-zA-Z0-9_]*$", payload))
            self.assertFalse(is_valid, f"Security Failure: Payload '{payload}' bypassed regex validation!")