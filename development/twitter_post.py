"""
twitter_post.py
"""

import requests


class ServerManager:
    def __init__(self):
        """
        Initialization method for ServerManager
        data:
            bearer_token:string (The authentication token for the Twitter API)
            headers:dict (A dictionary of headers for the HTTPS request)
        return:
            None
        """
        self.bearer_token = input('input your bearer token')  # get the bearer token
        self.headers = self._createHTTPSHeader(self.bearer_token)  # create headers
        self.url = None
        self.response = None

    def buildServerRequest(self, param):
        """
        A method that builds the server request for the Twitter API
        data:
            url:string (The url that will be queried)
            response:JSON (Returns the response in JSON format, to be parsed later)

        """
        self.url = self._createURL(param)  # get the URL
        self.response = self._getResponse()  # get the response

    def _createURL(self, param):
        """
        A method that geenrates the URL to be queried by formatting the parameters, and then returns it
        data:
            param:string (Search parameters)
            url:string (URL to be queried)
        return:
            string
        """
        # generate the URL
        url = f'https://api.twitter.com/1.1/statuses/show/{param}.json'
        return url

    def _createHTTPSHeader(self, bearer_token):
        """
        A method that create HTTPS headers for the request made above
        data:
            bearer_token:string
            headers:dict
        return:
            dict
        """
        # generate the HTTPS header
        headers = {"Authorization": "Bearer {}".format(bearer_token)}
        return headers

    def _getResponse(self):
        """
        A method that queries the server and gets its response
        data:
            response:requests.request (The response request)
        return:
            JSON (the response in JSON format)
        """
        # create header
        response = requests.request("GET", self.url, headers=self.headers)
        # if the response has an error (anything that is not a code of 200 is an error)
        if response.status_code != 200:
            return False
        # return the response if there is no error
        return response.json()


class ClientManager:
    def __init__(self):
        """
        Empty upon initalization.
        data:
            None
        return:
            None
        """
        self.param = ''

    def getQuery(self, param):
        """
        A method to get the user's query as a parameter
        data:
            param:string (user input)
        return:
            None
        """
        self.param = int(param)

    def callServer(self, other):
        """
        A simple method to build the server request. Does not return anything, just calls another object's method
        data:
            other:ServerManager
        return:
            None
        """
        other.buildServerRequest(self.param)


def main():
    # create ServerManager, Interpreter, ClientManager objects
    server = ServerManager()
    user = ClientManager()

    # call the getQuery() method
    user.getQuery(1221957211913457664)
    # build the server response
    user.callServer(server)
    # format and print hte server response
    import pprint

    pprint.pprint(server.response)
