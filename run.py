import pprint
from argparse import ArgumentParser
from routes import app
pp = pprint.PrettyPrinter(indent=4)

parser = ArgumentParser()
parser.add_argument('-H', '--host', default='127.0.0.1')
parser.add_argument('-p', '--port', default=5000, type=int)
args = parser.parse_args()

app.run(host=args.host, port=args.port, debug=True)
