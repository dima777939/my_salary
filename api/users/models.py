import sqlalchemy
from sqlalchemy import Boolean, Column, Integer, String, DateTime, MetaData, Table


metadata = MetaData()


User = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("username", String, unique=True, nullable=False, index=True),
    Column("hashed_password", String, nullable=False),
    Column("first_name", String, nullable=False),
    Column("last_name", String, nullable=False),
    Column("email", String, nullable=False, unique=True, index=True),
    Column("rate_an_hour", Integer, nullable=False),
    Column("date_increased", DateTime, nullable=False),
    Column("is_active", Boolean, server_default=sqlalchemy.sql.expression.true()),
    Column("is_staff", Boolean, server_default=sqlalchemy.sql.expression.false()),
    Column("is_superuser", Boolean, server_default=sqlalchemy.sql.expression.false()),
)
