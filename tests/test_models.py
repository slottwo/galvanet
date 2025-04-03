from sqlalchemy import select

from galvanet.models import User


def test_user_creation(session):
    user = User(username="test", password="0000")

    session.add(user)
    session.commit()
    # session.refresh(user)

    result: User = session.scalar(select(User).where(User.username == "test"))

    assert result.id == 1
    assert result.username == "test"
