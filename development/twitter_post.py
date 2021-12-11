"""
twitter_post.py
"""

import requests


class ServerManager:
    """
    A class that deals with requesting the server

    Instance Attributes:
    - bearer_token: the API token key
    - headers: the headers for the HTTPS request
    - url: the URL to be queried
    - response: the server response

    Representation Invariants:
    -
    """
    def __init__(self) -> None:
        """Initializes the ServerManager class"""
        self.bearer_token = input('input your bearer token')  # get the bearer token
        self.headers = self._createHTTPSHeader(self.bearer_token)  # create headers
        self.url = None
        self.response = None

    def buildServerRequest(self, param: str) -> None:
        """Builds the serve request for the Twitter API."""
        self.url = self._createURL(param)  # get the URL
        self.response = self._getResponse()  # get the response

    def _createURL(self, param: str) -> str:
        """Returns the URL to be queried"""
        # generate the URL
        url = f'https://api.twitter.com/1.1/statuses/show/{param}.json'
        return url

    def _createHTTPSHeader(self, bearer_token: str) -> dict:
        """Returns a dict of the HTTPS headers for the request made above"""
        # generate the HTTPS header
        headers = {"Authorization": "Bearer {}".format(bearer_token)}
        return headers

    def _getResponse(self) -> str:
        """Returns the server response in JSON format"""
        # create header
        response = requests.request("GET", self.url, headers=self.headers)
        # if the response has an error (anything that is not a code of 200 is an error)
        if response.status_code != 200:
            return False
        # return the response if there is no error
        return response.json()


class ClientManager:
    """A class that deals with getting the id we wish to search on
        the api

        Instance Attributes:
        - param:
    """
    def __init__(self) -> None:
        """Initialize the ClientManager class
        """
        self.param = ''

    def getQuery(self, param) -> None:
        """
        Gets the user's query
        """
        self.param = int(param)

    def callServer(self, other: ServerManager) -> None:
        """Builds the server request"""
        other.buildServerRequest(self.param)
