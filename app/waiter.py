from waitress import serve
import api
serve(api.app, host='0.0.0.0', port=8080)