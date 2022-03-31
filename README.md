# Lifeband-Server-Threaded

The python3 threaded server is designed to handle file uploads for the UKRI lifeband project. When data is uploaded from a client using the script provided, it dispatches the incoming data directly to a file which it creates in the ./devices directory, as well as sending a 200 status message back to the client, before freeing up and listening on the port again. 

This makes sure that the client never has to wait while data is being processed or sent to a database, meaning it can be collected in real-time. 

The web server also provides protections against directory traversal attacks using urllib functions.

## Usage
```python3 server.py```
