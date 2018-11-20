import connexion


def echo(body):
    print(body)
    return body


def main():
    app = connexion.App(__name__)
    app.add_api('./openapi.yml')
    app.run(port=8080)


if __name__ == '__main__':
    main()
