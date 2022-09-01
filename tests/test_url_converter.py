from url_converter import BaseUrlConverter


def test_base():
    converter = BaseUrlConverter()
    assert (
        converter.convert('http://localhost/abc/123.html')
        == 'http://localhost/abc/123.html'
    )
    assert (
        converter.convert('http://localhost:80/abc/123.html')
        == 'http://localhost:80/abc/123.html'
    )
    assert (
        converter.convert('http://localhost/abc/123.html?d=4')
        == 'http://localhost/abc/123.html?d=4'
    )
    assert (
        converter.convert('http://localhost/abc/123.html#e')
        == 'http://localhost/abc/123.html#e'
    )


class ForceHttpsUrlConverter(BaseUrlConverter):
    def _convert_scheme(self, parts) -> str:
        return 'https'

def test_force_https():
    converter = ForceHttpsUrlConverter()
    assert (
        converter.convert('http://localhost/abc/123.html')
        == 'https://localhost/abc/123.html'
    )


class ModifyNetlocUrlConverter(BaseUrlConverter):
    def __init__(self, netloc: str):
        self.netloc = netloc

    def _convert_netloc(self, parts) -> str:
        return self.netloc

def test_modify_netloc():
    converter = ModifyNetlocUrlConverter('example.com')
    assert (
        converter.convert('http://localhost/abc/123.html')
        == 'http://example.com/abc/123.html'
    )


class SecureHostnameUrlConverter(BaseUrlConverter):
    def __init__(self, hostname: str):
        self.secure_hostname = hostname

    def _convert_scheme(self, parts) -> str:
        if parts.hostname == self.secure_hostname:
            return 'https'
        return parts.scheme

def test_secure_hostname():
    converter = SecureHostnameUrlConverter('securehost')
    assert (
        converter.convert('http://localhost/abc/123.html')
        == 'http://localhost/abc/123.html'
    )
    assert (
        converter.convert('http://securehost/abc/123.html')
        == 'https://securehost/abc/123.html'
    )
