#!/usr/bin/env python

# Copyright (c) 2014, Palo Alto Networks
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# Author: Brian Torres-Gil <btorres-gil@paloaltonetworks.com>

import logging
import pandevice
from base import PanObject, Root, MEMBER, ENTRY
from base import VarPath as Var

# import other parts of this pandevice package
import errors as err

# set logging to nullhandler to prevent exceptions if logging not enabled
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class VsysResources(PanObject):

    XPATH = "/import/resource"
    ROOT = Root.VSYS

    def __init__(self,
                 max_sessions=None,
                 max_security_rules=None,
                 max_nat_rules=None,
                 max_ssl_decryption_rules=None,
                 max_qos_rules=None,
                 max_application_override_rules=None,
                 max_pbf_rules=None,
                 max_cp_rules=None,
                 max_dos_rules=None,
                 max_site_to_site_vpn_tunnels=None,
                 max_concurrent_ssl_vpn_tunnels=None,
                 ):
        super(VsysResources, self).__init__(name=None)
        self.max_sessions = max_sessions
        self.max_security_rules = max_security_rules
        self.max_nat_rules = max_nat_rules
        self.max_ssl_decryption_rules = max_ssl_decryption_rules
        self.max_qos_rules = max_qos_rules
        self.max_application_override_rules = max_application_override_rules
        self.max_pbf_rules = max_pbf_rules
        self.max_cp_rules = max_cp_rules
        self.max_dos_rules = max_dos_rules
        self.max_site_to_site_vpn_tunnels = max_site_to_site_vpn_tunnels
        self.max_concurrent_ssl_vpn_tunnels = max_concurrent_ssl_vpn_tunnels

    @classmethod
    def vars(cls):
        return (
            Var("max-security-rules", vartype="int"),
            Var("max-nat-rules", vartype="int"),
            Var("max-ssl-decryption-rules", vartype="int"),
            Var("max-qos-rules", vartype="int"),
            Var("max-application-override-rules", vartype="int"),
            Var("max-pbf-rules", vartype="int"),
            Var("max-cp-rules", vartype="int"),
            Var("max-dos-rules", vartype="int"),
            Var("max-site-to-site-vpn-tunnels", vartype="int"),
            Var("max-concurrent-ssl-vpn-tunnels", vartype="int"),
            Var("max-sessions", vartype="int"),
        )


class Vsys(PanObject):
    """Virtual System (VSYS)"""

    XPATH = "/vsys"
    ROOT = Root.DEVICE
    SUFFIX = ENTRY

    def __init__(self, name, display_name=None):
        super(Vsys, self).__init__(name)
        self.display_name = display_name
        self.interface = []

    @classmethod
    def vars(cls):
        return (
            Var("display-name"),
            Var("import/network/interface", vartype="member", init=False)
        )

    def xpath_vsys(self):
        if self.name == "shared" or self.name is None:
            return "/config/shared"
        else:
            return "/config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='%s']" % self.name

    @property
    def vsys(self):
        return self.name

    @vsys.setter
    def vsys(self, value):
        self.name = value


class NTPServer(PanObject):
    """A primary or secondary NTP server"""
    # TODO: Add authentication
    # TODO: Add PAN-OS pre-7.0 support

    XPATH = "/ntp-servers/primary-ntp-server"

    def __init__(self, address=None):
        if type(self) == NTPServer:
            raise err.PanDeviceError("Do not instantiate class. Please use a subclass.")
        super(NTPServer, self).__init__(name=None)
        self.address = address

    @classmethod
    def vars(cls):
        return (
            Var("ntp-server-address", "address"),
        )


class NTPServerPrimary(NTPServer):
    """A primary NTP server

    Add to a SystemSettings object

    Attributes:
        address (str): IP address or hostname of DNS server
    """
    XPATH = "/ntp-servers/primary-ntp-server"


class NTPServerSecondary(NTPServer):
    """A secondary NTP server

    Add to a SystemSettings object

    Attributes:
        address (str): IP address or hostname of DNS server
    """
    XPATH = "/ntp-servers/secondary-ntp-server"


class SystemSettings(PanObject):

    ROOT = Root.DEVICE
    XPATH = "/deviceconfig/system"
    HA_SYNC = False
    CHILDTYPES = (
        NTPServerPrimary,
        NTPServerSecondary,
    )

    def __init__(self, **kwargs):
        super(SystemSettings, self).__init__()
        self.hostname = kwargs.pop("hostname", None)
        self.domain = kwargs.pop("domain", None)
        self.ip_address = kwargs.pop("ip_address", None)
        self.netmask = kwargs.pop("netmask", None)
        self.default_gateway = kwargs.pop("default_gateway", None)
        self.ipv6_address = kwargs.pop("ipv6_address", None)
        self.ipv6_default_gateway = kwargs.pop("ipv6_default_gateway", None)
        self.dns_primary = kwargs.pop("dns_primary", None)
        self.dns_secondary = kwargs.pop("dns_secondary", None)
        self.timezone = kwargs.pop("timezone", None)
        self.panorama = kwargs.pop("panorama", None)
        self.panorama2 = kwargs.pop("panorama2", None)
        self.login_banner = kwargs.pop("login_banner", None)
        self.update_server = kwargs.pop("update_server", None)

    @classmethod
    def vars(cls):
        return (
            Var("hostname"),
            Var("domain"),
            Var("ip-address"),
            Var("netmask"),
            Var("default-gateway"),
            Var("ipv6-address"),
            Var("ipv6-default-gateway"),
            Var("dns-setting/servers/primary", "dns_primary"),
            Var("dns-setting/servers/secondary", "dns_secondary"),
            Var("timezone"),
            Var("panorama-server", "panorama"),
            Var("panorama-server-2", "panorama2"),
            Var("login-banner"),
            Var("update-server"),
        )
