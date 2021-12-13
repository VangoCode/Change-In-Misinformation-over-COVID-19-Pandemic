"""
Requesting the server and getting tweet IDs to search on the API with the classes
ServerManager and ClientManager using the Requests Library.

Copyright and Usage Information
==================================================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2021 Ron Varshavsky and Elsie (Muhan) Zhu.
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

    Representation Invariants
        - self.bearer_token != ''
        - self.bearer_token is a valid token for the Twitter API
        - self.url != ''
        - self.url is a valid URL to ping the twitter API
        - self.response != ''
    """
    bearer_token: str
    headers: dict
    url: str
    response: str

    def __init__(self) -> None:
        """Initializes the ServerManager class"""
        self.bearer_token = input('input your bearer token')  # get the bearer token
        self.headers = {"Authorization": "Bearer {}".format(self.bearer_token)}  # create headers
        self.url = ''
        self.response = ''

    def build_server_request(self, param: str) -> None:
        """Builds the serve request for the Twitter API."""
        self.url = f'https://api.twitter.com/1.1/statuses/show/{param}.json'  # get the URL
        self.response = self._get_response()  # get the response

    def _get_response(self) -> str:
        """Returns the server response in JSON format"""
        # create header
        response = requests.request("GET", self.url, headers=self.headers)
        # if the response has an error (anything that is not a code of 200 is an error)
        if response.status_code != 200:
            return ''
        # return the response if there is no error
        return response.json()


class ClientManager:
    """A class that deals with getting the ID we wish to search on the API

    Instance Attributes:
    - param: the ID of the tweet
    """
    param: int

    def __init__(self) -> None:
        """Initialize the ClientManager class"""
        self.param = 0

    def get_query(self, param: str) -> None:
        """Gets the user's query"""
        self.param = int(param)

    def call_server(self, other: ServerManager) -> None:
        """Builds the server request"""
        other.build_server_request(str(self.param))


if __name__ == '__main__':
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # Leave this code uncommented when you submit your files.
    #
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['python_ta.contracts', 'requests'],
        'allowed-io': ['__init__'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })

    import python_ta.contracts

    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()
