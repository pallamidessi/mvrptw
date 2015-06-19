"""
File containing the implementation of a REST server to use with the GA.
"""

import SocketServer
import SimpleHTTPServer
import urlparse


class GetHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """
    This class implements a handler based on the BaseHTTPRequestHandler class.
    """

    def __init__(self):
        self.vehicle_list = []
        self.crew_list = []
        self.journey_list = []
        self.employee_list = []
        super()

    def do_GET(self):
        """
        Handles GET requests
        """
        print self.command
        return

    def create_vehicle(self):
        """
        Creates a vehicle if the request path is /VehicleCreate
        """
        return 'Success'

    def do_POST(self):
        """
        Handles POST requests
        """
        if self.path == '/VehicleCreate':
            self.wfile.write(self.create_vehicle())
        elif self.path == '/EmployeeCreate':
            print 'b'
        elif self.path == '/CrewCreate':
            print 'c'
        elif self.path == '/JourneyCreate':
            print 'd'
        else:
            print 'nothing'
        self.wfile.close()

    def do_PUT(self):
        """
        Handles PUT requests
        """
        print self.command

    def do_PATCH(self):
        """
        Handles PATCH requests
        """
        print self.command

    def do_DELETE(self):
        """
        Handles DELETE requests
        """
        print self.command


Handler = GetHandler
server = SocketServer.TCPServer(('127.0.0.1', 8080), Handler)

try:
    server.serve_forever()
except KeyboardInterrupt:
    print ' received, shutting down server'
    server.socket.close()
