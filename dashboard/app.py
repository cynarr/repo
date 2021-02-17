from coviddash.app import app


__all__ = ["server"]

server = app.server


if __name__ == '__main__':
    app.run_server(debug=True)
