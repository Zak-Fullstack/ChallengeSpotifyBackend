
@pytest.fixture
def app():
    from challengegroover import create_app
    app = create_app()
    return app