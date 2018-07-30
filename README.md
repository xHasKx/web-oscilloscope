# Web Oscilloscope Prototype

...as an experiment...

## Technologies

* Python >= 3.6
* udp server
* aiohttp
* websockets
* canvas

## In Short

* Python starts two servers: UDP and HTTP
* Server allocates memory for uint16_t points array
* Server receives UDP datagramms and updating points array
* "sender.py" script sends random points to UDP socket of the server
* Web browser opens page from HTTP server (index.html)
* index.html opens websocket to the server
* Server sends current points every 0.1 second to opened websocket
* index.html draws points on canvas on every server message

## How To Run

On Debian GNU/Linux:

    # clone repo and prepare:
    git clone https://github.com/xHasKx/web-oscilloscope
    cd web-oscilloscope
    python3 -m venv env
    . env/bin/activate

    # start server:
    ./server.py

    # send random data to server:
    ./sender.py

## How It Looks

[Youtube](https://youtu.be/kylLA-0pHLY)
