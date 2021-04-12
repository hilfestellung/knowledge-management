from km import create_app
from km.database import init_db

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        init_db()
    app.run(host='0.0.0.0', port=8080, debug=True)
