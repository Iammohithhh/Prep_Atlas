"""Serve ONLY public site assets, bound to this computer by default."""
import argparse
import os
import socket
import webbrowser
from urllib.request import urlopen
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT=Path(__file__).resolve().parent

class Server(ThreadingHTTPServer):
    allow_reuse_address = os.name != 'nt'

    def server_bind(self):
        if os.name == 'nt':
            # Windows SO_REUSEADDR can let two processes share the same port.
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        super().server_bind()

class Handler(SimpleHTTPRequestHandler):
    extensions_map={**SimpleHTTPRequestHandler.extensions_map,'.wasm':'application/wasm','.js':'application/javascript','.json':'application/json'}
    def end_headers(self):
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Referrer-Policy','strict-origin-when-cross-origin')
        super().end_headers()
    def log_message(self, format, *args):
        pass

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8765);p.add_argument('--host',default='127.0.0.1');p.add_argument('--open',action='store_true',help='Open the browser after binding the server.');args=p.parse_args()
    handler=partial(Handler,directory=str(ROOT/'site'))
    address=f'http://{args.host}:{args.port}'
    try:
        server=Server((args.host,args.port),handler)
    except OSError:
        # Double-clicking the launcher again should reopen this site's running server.
        if args.open and args.host in {'127.0.0.1','localhost'}:
            try:
                with urlopen(address,timeout=2) as response:
                    same_site=response.read(1024*1024)==(ROOT/'site/index.html').read_bytes()
                if same_site:
                    print(f'Prep Atlas is already running: {address}',flush=True)
                    webbrowser.open(address)
                    raise SystemExit(0)
            except (OSError,ValueError):
                pass
        raise
    with server:
        print(f'Prep Atlas ready: http://{args.host}:{args.port}',flush=True)
        if args.open:webbrowser.open(address)
        try:server.serve_forever()
        except KeyboardInterrupt:pass
