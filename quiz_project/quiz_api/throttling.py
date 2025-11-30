"""
Custom throttling classes for API rate limiting.

Provides specialized throttling for sensitive operations like login attempts.
"""

from rest_framework.throttling import AnonRateThrottle


class LoginRateThrottle(AnonRateThrottle):
    """
    Throttle for login attempts.

    Prevents brute force attacks by limiting login attempts.
    Rate: 10 attempts per hour from the same IP.
    """
    scope = 'login'
