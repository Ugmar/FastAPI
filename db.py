from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

engine = create_engine(url="sqlite:///data.db")

session = sessionmaker(engine)

class Base(DeclarativeBase):
    pass

class Chat(Base):
    __tablename__ = "chat"

    id: Mapped[int] = mapped_column(primary_key=True)
    ip_adress: Mapped[str] = mapped_column(index=True)

    prompt: Mapped[str]
    response: Mapped[str]


def get_user_request(ip_adress: str) -> list[Chat]:
    with session() as new_session:
        query = select(Chat).filter_by(ip_adress=ip_adress)
        response = new_session.execute(query)
        return response.scalars().all()

def add_request_data(ip_adress: str, prompt: str, response: str) ->None:
    with session() as new_session:
        new_requst =  Chat(
            ip_adress=ip_adress,
            prompt=prompt,
            response=response
        )

        new_session.add(new_requst)
        new_session.commit()
