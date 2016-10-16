#!/usr/bin/env python3
# vim: set fileencoding=utf-8

"""Define WifiUtilABC as various OS implementation spec."""

import logging
from abc import ABCMeta, abstractmethod


class WifiUtilABC(metaclass=ABCMeta):
    """
    Abstract class used for each OS implementation.
    
    To support the wifi functions in each OS, implementors should
    finish all the abstract method defined here.
    """

    _logger = None

    def __init__(self):

        self._logger = logging.getLogger('pywifi')

    @abstractmethod
    def scan(self, osobj):
        """Trigger the wifi interface to scan."""

    @abstractmethod
    def scan_results(self, osobj):
        """Get the AP list after scanning."""

    @abstractmethod
    def connect(self, osobj, profile):
        """Connect to the specified AP."""

    @abstractmethod
    def disconnect(self, osobj):
        """Disconnect to the specified AP."""

    @abstractmethod
    def add_network_profile(self, osobj, profile):
        """Add an AP profile for connecting to afterward."""

    @abstractmethod
    def network_profiles(self, osobj):
        """Get AP profiles."""

    @abstractmethod
    def remove_all_network_profiles(self, osobj):
        """Remove all the AP profiles."""

    @abstractmethod
    def status(self, osobj):
        """Get the wifi interface status."""

    @abstractmethod
    def interfaces(self):
        """Get the wifi interface lists."""
