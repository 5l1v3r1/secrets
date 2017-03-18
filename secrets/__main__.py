import sys
from secrets import app

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    app.run(port=port)
