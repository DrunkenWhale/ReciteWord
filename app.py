from web import create_app

if __name__ == '__main__':
    app = create_app(__name__)
    app.debug = False
    app.run(port=7777, host="0.0.0.0")


