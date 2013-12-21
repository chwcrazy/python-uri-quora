"""Urilib.py is intended to aid in the manipulation of uri strings."""

import re

# This class stores a uri as its parts.


class Uri(object):

    """

    This class is meant to segment and store a uri as its
    parts. It utilizes regular expressions to parse an input uri string and
    identify each field. Alternatively, each field can be manually set or
    retrieved via properties created for each.

    """

    schemes = ['http', 'https', 'ftp', 'mailto']
    hostnamePattern = '((\w|-^_@)+\.)+[a-z]+(:[0-9]{2,5})?'
    pathPattern = '(/{1}[a-zA-Z]+)+(\.[a-z]+)?'

    def __init__(self, uriString='', delimeter='&'):

        self._paramDelimeter = delimeter
        self._scheme = ''
        self._hostname = ''
        self._path = ''
        self._params = {}
        self._urlFragment = ''
        self._username = ''
        self._password = ''
        self._email = ''

        if len(uriString) > 0:
            self._scheme = self._findScheme(uriString)
            self._hostname = self._findHostname(
                self.hostnamePattern, uriString)
            self._path = self._findPath(self.pathPattern, uriString)
            self._params = self._findParams(uriString)
            self._urlFragment = self._findUrlFragment(uriString)

            # if FTP
            # Note: username/password should be in params for http/https
            # schemes
            if self._scheme == 'ftp':
                uidAndPwd = self._checkForUsernameAndPassword(uriString)
                self._username = uidAndPwd[0]
                self._password = uidAndPwd[1]

            # email addresses should only occur in mailto schemes
            if self._scheme == 'mailto':
                self._email = self._checkForEmail(uriString)

    # Properties for each field in a uri
    def get_scheme(self):
        return self._scheme

    def set_scheme(self, value):
        if value in self.schemes:
            self._scheme = value
    scheme = property(get_scheme, set_scheme)

    def get_hostname(self):
        return self._hostname

    def set_hostname(self, value):
        match = re.search(self.hostnamePattern, value)
        if match:
            self._hostname = match.group()
    hostname = property(get_hostname, set_hostname)

    def get_path(self):
        return self._path

    def set_path(self, value):
        match = re.search(self.pathPattern, value)
        if match:
            self._path = match.group()
    path = property(get_path, set_path)

    def get_params(self):
        return self._params

    def set_params(self, value):
        self._params = value
    params = property(get_params, set_params)

    def get_paramDelimeter(self):
        return self._paramDelimeter

    def set_paramDelimeter(self, value):
        self._paramDelimeter = value
    paramDelimeter = property(get_paramDelimeter, set_paramDelimeter)

    def get_urlFragment(self):
        return self._urlFragment

    def set_urlFragment(self, value):
        self._urlFragment = value
    urlFragment = property(get_urlFragment, set_urlFragment)

    def get_username(self):
        return self._username

    def set_username(self, value):
        self._username = value
    username = property(get_username, set_username)

    def get_password(self):
        return self._password

    def set_password(self, value):
        self._password = value
    password = property(get_password, set_password)

    def get_email(self):
        return self._email

    def set_email(self, value):
        self._email = value
    email = property(get_email, set_email)

    def addOrUpdateParam(self, paramName, paramValue):
        self._params[paramName] = paramValue

    def addOrUpdateParams(self, paramDict):
        for k, v in paramDict.iteritems():
            self._params[k] = v

    def getTLD(self):
        """Splits the hostname and returns the chars after the period."""
        if len(self._hostname) > 0:
            return self._hostname.rsplit('.', 1)[1]

        return ''

    def fullString(self):
        """Returns the full uri string."""
        if self._scheme == 'mailto':
            return self._scheme + ':' + self._email

        fullUri = self._scheme + '://'
        if self._scheme == 'ftp':
            fullUri = fullUri + self._username
            if len(self._password) > 0:
                fullUri = fullUri + ':' + self._password

            fullUri = fullUri + '@'

        fullUri = fullUri + self._hostname + self._path + '?' + \
            self._getParamString() + '#' + self._urlFragment

        return fullUri

    def allFields(self):
        """Returns a dictionary with all of the identified fields."""
        return {'scheme': self._scheme,
                'hostname': self._hostname,
                'path': self._path,
                'params': self._params,
                'urlFragment': self._urlFragment,
                'paramDelimeter': self._paramDelimeter,
                'username': self._username,
                'password': self._password,
                'email': self._email}

    def _getParamString(self):
        """Returns a string of the listed parameters."""
        paramString = ''
        if len(self.params) > 0:
            for k, v in self._params:
                paramString += str(k) + '=' + str(v) + self._paramDelimeter

            # do not return trailing parameter delimeter
            return paramString.rsplit(self.paramDelimeter, 1)[0]

        return paramString

    def showParamString(self):
        print self._getParamString()

    def _findScheme(self, uri):
        """
        Tries to find the scheme of the input uri string.
        Since the scheme must be in the beginning of the string,
        it looks for the first ':' and checks if the characters
        before it match a string in the global schemes list.
        else returns an empty scheme.

        """
        if len(uri) > 0:
            schemeEnd = uri.find(':')
            if schemeEnd > 0:
                if (uri[:schemeEnd] in self.schemes):
                    return uri[:schemeEnd].lower()

        return ''

    def _findHostname(self, hostnamePattern, uri):
        """
        Checks for the hostname pattern, returns the matching string if found.

        Match one or more characters followed by a period
        one or more times, followed by one or more chars (domain)
        followed by an optional port, between 2 and 5 digits

        """
        match = re.search(hostnamePattern, uri)
        if match:
            return match.group()
        return ''

    def _findPath(self, pathPattern, uri):
        """
        Checks for the path pattern, returns the matching string if found.

        Looks for a single forward slash
        followed by one or more chars
        and optionally ends with a period followed by
        any number of lowercase letters.

        """
        for match in re.finditer(pathPattern, uri):
            pathGroup = match.group()
            prevChar = uri.find(pathGroup) - 1
            if uri[prevChar] is not None and uri[prevChar] != '/':
                return pathGroup
        return ''

    def _findParams(self, uri):
        """

        Creates a substring of the uri after the path string ends
        and searches through it for the parameters.

        """
        if len(self.path) > 0:
            pathStart = uri.rfind(self.path)
            startIndex = pathStart + len(self.path)
            # assume there is a char, usually a '?' between end of path and
            # start of params
            paramsString = uri[startIndex + 1:]
            paramsPattern = '((\w+=(\w|\W)+)' + \
                self.paramDelimeter + ')*(\w+=(\w|\W^#)+)'
            match = re.search(paramsPattern, paramsString)
            if match:
                paramDict = {}
                paramsList = match.group().split(self._paramDelimeter)
                for parameter in paramsList:
                    parameterSplit = parameter.split('=')
                    paramDict[parameterSplit[0]] = parameterSplit[1]
                return paramDict
        return {}

    def _findUrlFragment(self, uri):
        if len(uri) > 0 and self._hostname is not '':
            fragmentStart = uri.rfind('#')
            if fragmentStart > 0:
                return uri[(fragmentStart + 1):]
        return ''

    def _checkForEmail(self, uri):
        emailStart = uri.rfind(':') + 1
        emailString = uri[emailStart:]
        emailPattern = '(\w|\W^@)+@([a-z]+\.)+[a-z]+'
        match = re.search(emailPattern, emailString)
        if match:
            return match.group()
        return ''

    def _checkForUsernameAndPassword(self, uri):
        uidAndPwd = ['', '']
        start = uri.find('//') + 2  # Get the char after the '//'
        end = uri.find('@')
        if (start >= 0) and (end >= 0) and (end > start):
            creds = uri[start:end]
            if creds[0] is not ':':
                credList = creds.split(':')
                uidAndPwd[0] = credList[0]
                if len(credList) > 1:
                    uidAndPwd[1] = credList[1]

        return uidAndPwd
