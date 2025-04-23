import datetime

from sqlalchemy import BigInteger, Boolean, Date, Integer, Sequence, String, UniqueConstraint, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass

class UserData(Base):
    __tablename__ = "user_data"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(30), nullable=True)
    lang: Mapped[str] = mapped_column(String(5), default="en-EN")
    message_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    invite_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    voice_time: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    bump_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    tag: Mapped[str] = mapped_column(String, nullable=True)
    biography: Mapped[str] = mapped_column(String, nullable=True)
    birthday_date: Mapped[str] = mapped_column(Date, nullable=True)

class NuclearData(Base):
    __tablename__ = "nuclear_data"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(30), nullable=True)
    new_user: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    nuclear_mode: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    bomb_start_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    mivina_start_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    bomb_cd: Mapped[str] = mapped_column(Date, nullable=True, default="")
    mivina_cd: Mapped[str] = mapped_column(Date, nullable=True, default="")

class NuclearLogs(Base):
    __tablename__ = "nuclear_logs"

    id: Mapped[int] = mapped_column(Integer, Sequence('nuclear_logs_id_seq'), primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    username: Mapped[str] = mapped_column(String(32), nullable=True)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False, server_default=func.current_date())
    used: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    log_type: Mapped[str] = mapped_column(String(10), nullable=False)

class GuildConfig(Base):
    __tablename__ = "guild_config"

    guild_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    guild_name: Mapped[str] = mapped_column(String(32), nullable=True)
    lang: Mapped[str] = mapped_column(String(5), default="en-EN")
    welcome_channel_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    welcome_message: Mapped[str] = mapped_column(String, nullable=True)
    welcome_role_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    private_category_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    private_voice_id: Mapped[int] = mapped_column(BigInteger, nullable=True)

class EmbedConfig(Base):
    __tablename__ = "embed_config"

    id: Mapped[int] = mapped_column(Integer, Sequence('embed_config_id_seq', start=1, increment=1), primary_key=True)
    guild_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    embed_key: Mapped[str] = mapped_column(String, nullable=True)
    title: Mapped[str] = mapped_column(String(256), nullable=True)
    descrition: Mapped[str] = mapped_column(String(4096), nullable=True)
    footer_text: Mapped[str] = mapped_column(String(2048), nullable=True)
    author_name: Mapped[str] = mapped_column(String(256), nullable=True)
    image_url: Mapped[str] = mapped_column(String(256), nullable=True)
    thumbnail_url: Mapped[str] = mapped_column(String(256), nullable=True)
    footer_icon_url: Mapped[str] = mapped_column(String(256), nullable=True)
    color: Mapped[str] = mapped_column(String(256), nullable=True)
    url: Mapped[str] = mapped_column(String(256), nullable=True)

    __table_args__ = (
        UniqueConstraint('guild_id', 'embed_key', name='uix_guild_embed_key'),
    )
