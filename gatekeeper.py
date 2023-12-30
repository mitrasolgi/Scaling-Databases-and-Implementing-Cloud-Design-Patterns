# gatekeeper.py

class Gatekeeper:
    def __init__(self, proxy):
        self.proxy = proxy

    def process_request(self, query_type):
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
