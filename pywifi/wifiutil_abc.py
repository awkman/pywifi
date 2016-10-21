#!/usr/bin/env python3
# vim: set fileencoding=utf-8

"""Define WifiUtilABC as various OS implementation spec."""

import logging
import abc


# For compatible with Python 2 *and* 3
ABC = abc.ABCMeta('ABC', (object,), {})

class WifiUtilABC(ABC):
    """
    Abstract class used for each OS implementation.
    
    To support the wifi functions in each OS, implementors should
    finish all the abstract method defined here.
    """


    _logger = None

    def __init__(self):

        self._logger = logging.getLogger('pywifi')

    @abc.abstractmethod
    def scan(self, osobj):
        """Trigger the wifi interface to scan."""

    @abc.abstractmethod
    def scan_results(self, osobj):
        """Get the AP list after scanning."""

    @abc.abstractmethod
    def connect(self, osobj, profile):
        """Connect to the specified AP."""

    @abc.abstractmethod
    def disconnect(self, osobj):
        """Disconnect to the specified AP."""

    @abc.abstractmethod
    def add_network_profile(self, osobj, profile):
        """Add an AP profile for connecting to afterward."""

    @abc.abstractmethod
    def network_profiles(self, osobj):
        """Get AP profiles."""

    @abc.abstractmethod
    def remove_all_network_profiles(self, osobj):
        """Remove all the AP profiles."""

    @abc.abstractmethod
    def status(self, osobj):
        """Get the wifi interface status."""

    @abc.abstractmethod
    def interfaces(self):
        """Get the wifi interface lists."""
