import datetime as dt


def test_get_simple(example_api_client):
    assert example_api_client.api.get_simple() == {"Hello": "World"}


def test_post_simple(example_api_client):
    assert example_api_client.api.post_simple(42) == 42


def test_post_dto(example_api_client):
    from swclient.apis.api.post_dto import PostDTO

    now = dt.datetime.now()

    assert example_api_client.api.post_dto(
        PostDTO(
            string="test string",
            number=42,
            date=now.date(),
            datetime=now,
        )
    ) == PostDTO(
        string="test string",
        number=42,
        date=now.date(),
        datetime=now,
    )
