"""
gatekeeper.py

This module defines the Gatekeeper class, responsible for processing database queries.
The Gatekeeper utilizes a provided proxy to route and execute SQL queries.

Usage:
    1. Import the Gatekeeper class from this module.
    2. Create an instance of the Gatekeeper, passing a proxy as a parameter.
    3. Call the `process_request` method with the query type to initiate query processing.

Example:
    from gatekeeper import Gatekeeper
    from my_proxy_module import MyProxy

    # Create an instance of the proxy (MyProxy should be replaced with the actual proxy class)
    proxy_instance = MyProxy()

    # Create an instance of the Gatekeeper with the proxy
    gatekeeper = Gatekeeper(proxy_instance)

    # Process a write query
    gatekeeper.process_request('write')

Note:
    - The process_request method currently contains a sample SQL query for insertion.
      Modify the method and queries as needed for your specific use case.
"""

class Gatekeeper:
    def __init__(self, proxy):
        """
             Initializes the Gatekeeper with a given proxy.

             Parameters:
                 proxy (object): An instance of the proxy class responsible for routing and executing SQL queries.
             """
        self.proxy = proxy

    def process_request(self, query_type):
        """
              Processes a database query based on the provided query type.

              Parameters:
                  query_type (str): The type of the database query ('read' or 'write').

              Example:
                  gatekeeper.process_request('write')
              """
        data_to_insert = [
            ("John Doe", 25, "john.doe@example.com"),
            ("Mark Smith", 30, "mark.smith@example.com"),
            ("Alice Johnson", 28, "alice.johnson@example.com"),
            ("Bob Brown", 35, "bob.brown@example.com"),
        ]

        # Construct the query with values included
        query = "INSERT INTO incoming_requests (name, age, email) VALUES "
        values_strings = [f"('{name}', {age}, '{email}')" for name, age, email in data_to_insert]
        query += ", ".join(values_strings)


        self.proxy.route_query(query)
