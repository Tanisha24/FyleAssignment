from app import app
from app import *

if __name__ == '__main__':
    init_db()
    app.run(host='127.0.0.1', port=8080, debug=True)
