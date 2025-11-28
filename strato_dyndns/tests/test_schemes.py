"""Tests for DynDNS client schemes and implementations."""

import pytest

from strato_dyndns import DynDNSClient
from strato_dyndns.clients import (
    DynDNSClientInitException,
    StratoClient,
    NamecheapClient,
)
from strato_dyndns.clients.strato_client import (
    StratoClientInitData,
    StratoClientInitError,
    StratoOutputAnalyzer,
)
from strato_dyndns.clients.namecheap_client import (
    NamecheapClientInitData,
    NamecheapClientInitError,
    NamecheapOutputAnalyzer,
)
from strato_dyndns.schema import StratoSchema, NamecheapSchema


class TestStratoClient:
    """Tests for StratoClient."""

    def test_initialization(self):
        """Test StratoClient initializes properly."""
        client = StratoClient()
        assert not client.is_initialized()

    def test_set_authentication(self):
        """Test setting authentication credentials."""
        client = StratoClient()
        client.set_authentication("testuser", "testpass")
        url = client.update_url()
        assert "testuser:testpass" in url

    def test_set_domain(self):
        """Test setting domain."""
        client = StratoClient()
        client.set_domain("test.example.com")
        url = client.update_url()
        assert "hostname=test.example.com" in url

    def test_set_ip_addresses(self):
        """Test setting IP addresses."""
        client = StratoClient()
        client.set_ip_addresses(["192.168.1.1", "192.168.1.2"])
        url = client.update_url()
        assert "myip=192.168.1.1,192.168.1.2" in url

    def test_is_initialized_complete(self):
        """Test that client reports fully initialized."""
        client = StratoClient()
        client.set_authentication("user", "pass")
        client.set_domain("domain.com")
        client.set_ip_addresses(["1.2.3.4"])
        assert client.is_initialized()


class TestStratoClientInitData:
    """Tests for StratoClientInitData."""

    def test_valid_data(self):
        """Test initialization with valid data."""
        data = {
            "username": "testuser",
            "password": "testpass",
            "domain": "test.example.com",
            "ip_addresses": ["192.168.1.1"],
        }
        init_data = StratoClientInitData(data)
        assert init_data.username == "testuser"
        assert init_data.password == "testpass"
        assert init_data.domain == "test.example.com"
        assert init_data.ip_addresses == ["192.168.1.1"]

    def test_missing_fields(self):
        """Test initialization with missing fields raises error."""
        data = {"username": "testuser"}
        with pytest.raises(StratoClientInitError):
            StratoClientInitData(data)


class TestStratoOutputAnalyzer:
    """Tests for StratoOutputAnalyzer."""

    def test_good_response(self):
        """Test analyzing successful update response."""
        analyzer = StratoOutputAnalyzer("good 192.168.1.1")
        analyzer.analyze()
        assert analyzer.status == "OK"
        assert "successfully" in analyzer.response.lower()

    def test_nochg_response(self):
        """Test analyzing no change response."""
        analyzer = StratoOutputAnalyzer("nochg 192.168.1.1")
        analyzer.analyze()
        assert analyzer.status == "OK"
        assert "no changes" in analyzer.response.lower()

    def test_badauth_response(self):
        """Test analyzing bad authentication response."""
        analyzer = StratoOutputAnalyzer("badauth")
        analyzer.analyze()
        assert analyzer.status == "ERROR"
        assert "authentication" in analyzer.response.lower()

    def test_unknown_response(self):
        """Test analyzing unknown response."""
        analyzer = StratoOutputAnalyzer("unknowncode")
        analyzer.analyze()
        assert analyzer.status == "ERROR"
        assert "unknown" in analyzer.response.lower()


class TestNamecheapClient:
    """Tests for NamecheapClient."""

    def test_initialization(self):
        """Test NamecheapClient initializes properly."""
        client = NamecheapClient()
        assert not client.is_initialized()

    def test_set_authentication(self):
        """Test setting authentication credentials."""
        client = NamecheapClient()
        client.set_authentication("example.com", "testpass")
        url = client.update_url()
        assert "domain=example.com" in url
        assert "password=testpass" in url

    def test_is_initialized_complete(self):
        """Test that client reports fully initialized."""
        client = NamecheapClient()
        client.set_authentication("example.com", "pass")
        client.set_domain("@")
        client.set_ip_addresses(["1.2.3.4"])
        assert client.is_initialized()


class TestNamecheapClientInitData:
    """Tests for NamecheapClientInitData."""

    def test_valid_data(self):
        """Test initialization with valid data."""
        data = {
            "username": "example.com",
            "password": "testpass",
            "domain": "@",
            "ip_addresses": ["192.168.1.1"],
        }
        init_data = NamecheapClientInitData(data)
        assert init_data.username == "example.com"
        assert init_data.password == "testpass"
        assert init_data.domain == "@"
        assert init_data.ip_addresses == ["192.168.1.1"]

    def test_multiple_ip_addresses_error(self):
        """Test initialization with multiple IP addresses raises error."""
        data = {
            "username": "example.com",
            "password": "testpass",
            "domain": "@",
            "ip_addresses": ["192.168.1.1", "192.168.1.2"],
        }
        with pytest.raises(NamecheapClientInitError):
            NamecheapClientInitData(data)

    def test_ipv6_address_error(self):
        """Test initialization with IPv6 address raises error."""
        data = {
            "username": "example.com",
            "password": "testpass",
            "domain": "@",
            "ip_addresses": ["::1"],
        }
        with pytest.raises(NamecheapClientInitError):
            NamecheapClientInitData(data)


class TestNamecheapOutputAnalyzer:
    """Tests for NamecheapOutputAnalyzer."""

    def test_success_response(self):
        """Test analyzing successful response."""
        xml_response = """<?xml version="1.0"?>
        <interface-response>
            <Command>SETDNSHOST</Command>
            <ErrCount>0</ErrCount>
            <responses>
                <response>
                    <ResponseString>Success</ResponseString>
                </response>
            </responses>
        </interface-response>"""
        analyzer = NamecheapOutputAnalyzer(xml_response)
        analyzer.analyze()
        assert analyzer.status == "OK"
        assert analyzer.response == "Success"

    def test_error_response(self):
        """Test analyzing error response."""
        xml_response = """<?xml version="1.0"?>
        <interface-response>
            <Command>SETDNSHOST</Command>
            <ErrCount>1</ErrCount>
            <responses>
                <response>
                    <ResponseString>Invalid password</ResponseString>
                </response>
            </responses>
        </interface-response>"""
        analyzer = NamecheapOutputAnalyzer(xml_response)
        analyzer.analyze()
        assert analyzer.status == "ERROR"
        assert analyzer.response == "Invalid password"


class TestDynDNSClient:
    """Tests for main DynDNSClient."""

    def test_create_strato_client(self):
        """Test creating DynDNS client for Strato."""
        client = DynDNSClient("strato")
        assert client is not None

    def test_create_namecheap_client(self):
        """Test creating DynDNS client for Namecheap."""
        client = DynDNSClient("namecheap")
        assert client is not None

    def test_unsupported_provider(self):
        """Test creating client for unsupported provider raises exception."""
        with pytest.raises(DynDNSClientInitException):
            DynDNSClient("unknown_provider")

    def test_init_data(self):
        """Test initializing client with data."""
        client = DynDNSClient("strato")
        data = {
            "username": "testuser",
            "password": "testpass",
            "domain": "test.example.com",
            "ip_addresses": ["192.168.1.1"],
        }
        client.init_data(data)
        # Should not raise exception

    def test_update_record_before_init(self):
        """Test updating record before initialization raises exception."""
        client = DynDNSClient("strato")
        with pytest.raises(DynDNSClientInitException):
            client.update_record()


class TestSchemas:
    """Tests for schema definitions."""

    def test_strato_schema_url(self):
        """Test Strato schema has proper URL format."""
        assert "<username>" in StratoSchema.UPDATE_URL
        assert "<password>" in StratoSchema.UPDATE_URL
        assert "<domain>" in StratoSchema.UPDATE_URL
        assert "<ip-address>" in StratoSchema.UPDATE_URL
        assert "dyndns.strato.com" in StratoSchema.UPDATE_URL

    def test_namecheap_schema_url(self):
        """Test Namecheap schema has proper URL format."""
        assert "<host>" in NamecheapSchema.UPDATE_URL
        assert "<domain_name>" in NamecheapSchema.UPDATE_URL
        assert "<password>" in NamecheapSchema.UPDATE_URL
        assert "<ip_address>" in NamecheapSchema.UPDATE_URL
        assert "dynamicdns.park-your-domain.com" in NamecheapSchema.UPDATE_URL
