import unittest
from urilib import Uri


class TestUriLib(unittest.TestCase):

    def setUp(self):
        pass

    def test_valid_http(self):
        url = 'http://www.standardtreasury.com'
        u = Uri(url)
        self.assertEqual('http', u.scheme)
        self.assertEqual('www.standardtreasury.com', u.hostname)

    def test_valid_https(self):
        url = 'https://www.google.com'
        u = Uri(url)
        self.assertEqual('https', u.scheme)
        self.assertEqual('www.google.com', u.hostname)

    def test_valid_ftp(self):
        url = 'ftp://www.myserver.com'
        u = Uri(url)
        self.assertEqual('ftp', u.scheme)
        self.assertEqual('www.myserver.com', u.hostname)

    def test_valid_mailto(self):
        uri = 'mailto:rohitrajan@live.com'
        u = Uri(uri)
        self.assertEqual('mailto', u.scheme)
        self.assertEqual('rohitrajan@live.com', u.email)

    def test_valid_http_with_path(self):
        url = 'http://www.standardtreasury.com/main/page.html'
        u = Uri(url)
        self.assertEqual('http', u.scheme)
        self.assertEqual('www.standardtreasury.com', u.hostname)
        self.assertEqual('/main/page.html', u.path)

    def test_valid_http_with_params(self):
        url = 'http://www.standardtreasury.com?param1=none'
        u = Uri(url)
        self.assertEqual('http', u.scheme)
        self.assertEqual('www.standardtreasury.com', u.hostname)
        self.assertEqual({}, u.params)

    def test_valid_http_with_fragment(self):
        url = 'http://www.standardtreasury.com#20131116'
        u = Uri(url)
        self.assertEqual('http', u.scheme)
        self.assertEqual('www.standardtreasury.com', u.hostname)
        self.assertEqual('20131116', u.urlFragment)

    def test_valid_http_with_path_and_params(self):
        url = 'http://www.standardtreasury.com/path.xyz?param1=hello&p2=W0rld'
        u = Uri(url)
        self.assertEqual('http', u.scheme)
        self.assertEqual('www.standardtreasury.com', u.hostname)
        self.assertEqual('/path.xyz', u.path)
        self.assertIn('param1', u.params.keys())
        self.assertIn('p2', u.params.keys())
        self.assertEqual('hello', u.params['param1'])
        self.assertEqual('W0rld', u.params['p2'])

    def test_valid_http_with_path_and_fragment(self):
        url = 'http://www.standardtreasury.com/path/to/page.abc#20131116'
        u = Uri(url)
        self.assertEqual('http', u.scheme)
        self.assertEqual('www.standardtreasury.com', u.hostname)
        self.assertEqual('/path/to/page.abc', u.path)
        self.assertEqual('20131116', u.urlFragment)

    def test_valid_http_with_params_and_fragment(self):
        url = 'http://www.standardtreasury.com?param1=hello&p2=W0rld#20131116'
        u = Uri(url)
        self.assertEqual('http', u.scheme)
        self.assertEqual('www.standardtreasury.com', u.hostname)
        self.assertEqual({}, u.params)
        self.assertEqual('20131116', u.urlFragment)

    def test_valid_http_with_path_and_params_and_fragment(self):
        url = 'http://www.myserver.com/path.x?param1=hello&p2=W0rld#20131116'
        u = Uri(url)
        self.assertEqual('http', u.scheme)
        self.assertEqual('www.myserver.com', u.hostname)
        self.assertEqual('/path.x', u.path)
        self.assertIn('param1', u.params.keys())
        self.assertIn('p2', u.params.keys())
        self.assertEqual('hello', u.params['param1'])
        self.assertEqual('W0rld', u.params['p2'])
        self.assertEqual('20131116', u.urlFragment)

    def test_valid_https_with_path(self):
        url = 'https://www.standardtreasury.com/main/page.html'
        u = Uri(url)
        self.assertEqual('https', u.scheme)
        self.assertEqual('www.standardtreasury.com', u.hostname)
        self.assertEqual('/main/page.html', u.path)

    def test_valid_https_with_params(self):
        url = 'https://www.standardtreasury.com?param1=none'
        u = Uri(url)
        self.assertEqual('https', u.scheme)
        self.assertEqual('www.standardtreasury.com', u.hostname)
        self.assertEqual({}, u.params)

    def test_valid_https_with_fragment(self):
        url = 'https://www.standardtreasury.com#20131116'
        u = Uri(url)
        self.assertEqual('https', u.scheme)
        self.assertEqual('www.standardtreasury.com', u.hostname)
        self.assertEqual('20131116', u.urlFragment)

    def test_valid_https_with_path_and_params(self):
        url = 'https://www.myserver.com/path/to/page.xyz?param1=hello&p2=W0rld'
        u = Uri(url)
        self.assertEqual('https', u.scheme)
        self.assertEqual('www.myserver.com', u.hostname)
        self.assertEqual('/path/to/page.xyz', u.path)
        self.assertIn('param1', u.params.keys())
        self.assertIn('p2', u.params.keys())
        self.assertEqual('hello', u.params['param1'])
        self.assertEqual('W0rld', u.params['p2'])

    def test_valid_https_with_path_and_fragment(self):
        url = 'https://www.standardtreasury.com/path/to/page.abc#20131116'
        u = Uri(url)
        self.assertEqual('https', u.scheme)
        self.assertEqual('www.standardtreasury.com', u.hostname)
        self.assertEqual('/path/to/page.abc', u.path)
        self.assertEqual('20131116', u.urlFragment)

    def test_valid_https_with_params_and_fragment(self):
        url = 'https://www.standardtreasury.com?param1=hello&p2=W0rld#20131116'
        u = Uri(url)
        self.assertEqual('https', u.scheme)
        self.assertEqual('www.standardtreasury.com', u.hostname)
        self.assertEqual({}, u.params)
        self.assertEqual('20131116', u.urlFragment)

    def test_valid_https_with_path_and_params_and_fragment(self):
        url = 'https://www.myserver.com/path.xyz?param=hello&p2=W0rld#20131116'
        u = Uri(url)
        self.assertEqual('https', u.scheme)
        self.assertEqual('www.myserver.com', u.hostname)
        self.assertEqual('/path.xyz', u.path)
        self.assertIn('param', u.params.keys())
        self.assertIn('p2', u.params.keys())
        self.assertEqual('hello', u.params['param'])
        self.assertEqual('W0rld', u.params['p2'])
        self.assertEqual('20131116', u.urlFragment)

    def test_valid_ftp_with_username(self):
        url = 'ftp://rohit@www.myserver.com'
        u = Uri(url)
        self.assertEqual('ftp', u.scheme)
        self.assertEqual('www.myserver.com', u.hostname)
        self.assertEqual('rohit', u.username)

    def test_valid_ftp_with_password(self):
        url = 'ftp://:mypassword@www.myserver.com'
        u = Uri(url)
        self.assertEqual('ftp', u.scheme)
        self.assertEqual('www.myserver.com', u.hostname)
        self.assertEqual('', u.password)

    def test_valid_ftp_with_username_and_password(self):
        url = 'ftp://rohit:mypassword@www.myserver.com'
        u = Uri(url)
        self.assertEqual('ftp', u.scheme)
        self.assertEqual('www.myserver.com', u.hostname)
        self.assertEqual('rohit', u.username)
        self.assertEqual('mypassword', u.password)

    def test_custom_uri_object(self):
        u = Uri()
        u.scheme = 'asdf'
        self.assertEqual('', u.scheme)
        u.scheme = 'http'
        self.assertEqual('http', u.scheme)

        u.hostname = 'random'
        self.assertEqual('', u.hostname)
        u.hostname = 'random.site.com:80'
        self.assertEqual('random.site.com:80', u.hostname)

        u.path = 'mybadpath'
        self.assertEqual('', u.path)
        u.path = '/my/good/path'
        self.assertEqual('/my/good/path', u.path)

        u.urlFragment = 'anythingiwant'
        self.assertEqual('anythingiwant', u.urlFragment)

        u.addOrUpdateParam('k', 'v')
        self.assertIn('k', u.params.keys())
        myParams = {'p1': 'val1', 'paramTwo': 'Value2'}
        u.addOrUpdateParams(myParams)
        self.assertIn('p1', u.params.keys())
        self.assertIn('paramTwo', u.params.keys())
        self.assertEqual(u.params['p1'], 'val1')
        self.assertEqual(u.params['paramTwo'], 'Value2')
        u.params = myParams
        self.assertNotIn('k', u.params.keys())

    def test_uri_with_missing_scheme(self):
        url = 'standardtreasury.com'
        u = Uri(url)
        self.assertEqual('', u.scheme)
        self.assertEqual('standardtreasury.com', u.hostname)

        url = '/my/path/to/dir'
        u = Uri(url)
        self.assertEqual('', u.scheme)
        self.assertEqual('', u.hostname)
        self.assertEqual('/my/path/to/dir', u.path)

    def test_uri_with_missing_domain(self):
        url = 'http://'
        u = Uri(url)
        self.assertEqual('http', u.scheme)
        self.assertEqual('', u.hostname)

        url = 'https://my/path'
        u = Uri(url)
        self.assertEqual('https', u.scheme)
        self.assertEqual('', u.path)

    def test_uri_with_several_subdomains(self):
        url = 'http://my.very.long.hostname.co.uk'
        u = Uri(url)
        self.assertEqual('http', u.scheme)
        self.assertEqual('my.very.long.hostname.co.uk', u.hostname)
        self.assertEqual('uk', u.getTLD())

    def test_email_without_scheme(self):
        url = 'rohitrajan@live.com'
        u = Uri(url)
        self.assertEqual('', u.scheme)
        self.assertEqual('live.com', u.hostname)

    def test_random_string(self):
        url = 'ald1@!#!@!(1)'
        u = Uri(url)

        for val in u.params.itervalues():
            if len(val) == 1:
                self.assertEqual('&', val)  # For the parameter delimeter
            else:
                self.assertEqual(len(val), 0)


if __name__ == "__main__":
    unittest.main()
