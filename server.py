# copyright and author
__author__ = 'm@corporation9.com, shranav@corporation9.com'
__copyright__ = 'Copyright 2022, The Lifeband Project (UKRI Funded Research)'

# import HTTPServer, BaseHTTPRequestHandler
from http.server import HTTPServer, BaseHTTPRequestHandler
# import ThreadingMixIn
from socketserver import ThreadingMixIn
# import Path
from pathlib import Path
# import re, binascii
import re, binascii

PORT = 8080

# ThreadingHTTPServer is a subclass of HTTPServer
class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass

# HTTP request handler
class TLoggerHTTPHandler(BaseHTTPRequestHandler):
    # POST request
    def do_POST(self):
        dev_mac, bupload_id = map( # split and parse the device mac and upload id
            binascii.unhexlify, 
            re.search(
                r"dev ([0-9a-f]{12}) id ([0-9a-f]{8})",
                self.headers["User-Agent"]
            ).groups()
        )
        # get the upload ID from the request
        upload_id = int.from_bytes(bupload_id, "big") # convert the upload id into an integer

        # get the length of the request body
        rfile_len = int(self.headers["Content-Length"]) # get the file length

        # get the content disposition
        rfile_devpath = re.search(
            r"\"([\w\/.]*)\"",
            self.headers["Content-Disposition"]
        ).group(1)[1:]

        # get the file identifier
        rfile_wpath = Path(
            "devices",
            "mac_" + "".join(map("%02x".__mod__, dev_mac)),
            "upload_%08x" % upload_id,
            rfile_devpath
        )

        # print status
        print("recieved %s, saving to %s (%d bytes)" % (rfile_devpath, rfile_wpath, rfile_len))
        # create the directory if it doesn't exist
        rfile_wpath.parent.mkdir(parents=True, exist_ok=True)
        # open the file for writing
        rfile_wpath.write_bytes(self.rfile.read(rfile_len))
        # send the response
        self.send_response_only(200)

# main
def main():
    # create the server
    server = ThreadingHTTPServer(('0.0.0.0', PORT), TLoggerHTTPHandler)
    # print status
    print("running server...")
    # start the server
    server.serve_forever()

# run the main function
if __name__ == '__main__':
    # main function
    main()
