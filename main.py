import os
from app import app

if __name__ == "__main__":
    app.run(
    	debug=True,
    	host="0.0.0.0",
    	port=8080,
    	)
    # app.run()
    # from waitress import serve
    # # serve(app, listen='*:8080')
    # serve(app, host='0.0.0.0', port=80)
