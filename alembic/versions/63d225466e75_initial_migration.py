"""Initial migration

Revision ID: 63d225466e75
Revises: 
Create Date: 2025-03-14 07:32:28.174753

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '63d225466e75'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema — create all tables from scratch."""

    op.create_table(
        'user_data',
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('username', sa.String(length=30), nullable=True),
        sa.Column('lang', sa.String(length=5), nullable=False,
                  server_default=sa.text("'en-EN'::character varying")),
        sa.Column('message_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('invite_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('voice_time', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('bump_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('tag', sa.Text(), nullable=True),
        sa.Column('biography', sa.Text(), nullable=True),
        sa.Column('birthday_date', sa.Date(), nullable=True),
        sa.PrimaryKeyConstraint('user_id'),
    )

    op.create_table(
        'nuclear_data',
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('username', sa.String(length=30), nullable=True),
        sa.Column('new_user', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('nuclear_mode', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('bomb_start_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('mivina_start_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('bomb_cd', sa.Date(), nullable=True),
        sa.Column('mivina_cd', sa.Date(), nullable=True),
        sa.PrimaryKeyConstraint('user_id'),
    )

    op.create_table(
        'nuclear_logs',
        # Created with final column types to avoid redundant ALTERs below
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('username', sa.String(length=32), nullable=True),
        sa.Column('date', sa.Date(), nullable=False,
                  server_default=sa.text('CURRENT_DATE')),
        sa.Column('used', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('log_type', sa.String(length=10), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'guild_config',
        # baseline: without private_voice_id (added in 233b4ceb2929)
        #           and without private_category_id (added in 00e8df0f93b2)
        sa.Column('guild_id', sa.BigInteger(), nullable=False),
        sa.Column('guild_name', sa.String(length=32), nullable=True),
        sa.Column('lang', sa.String(length=5), nullable=False,
                  server_default=sa.text("'en-EN'::character varying")),
        sa.Column('welcome_channel_id', sa.BigInteger(), nullable=True),
        sa.Column('welcome_message', sa.String(), nullable=True),
        sa.Column('welcome_role_id', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('guild_id'),
    )


    op.create_table(
        'embed_config',
        # baseline: column was misspelled "descrition" (fixed in 82a61992e39a)
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('guild_id', sa.BigInteger(), nullable=False),
        sa.Column('embed_key', sa.String(), nullable=True),
        sa.Column('title', sa.String(length=256), nullable=True),
        sa.Column('descrition', sa.String(length=4096), nullable=True),   # intentional typo — fixed in later migration
        sa.Column('footer_text', sa.String(length=2048), nullable=True),
        sa.Column('author_name', sa.String(length=256), nullable=True),
        sa.Column('image_url', sa.String(length=256), nullable=True),
        sa.Column('thumbnail_url', sa.String(length=256), nullable=True),
        sa.Column('footer_icon_url', sa.String(length=256), nullable=True),
        sa.Column('color', sa.String(length=256), nullable=True),
        sa.Column('url', sa.String(length=256), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('guild_id', 'embed_key', name='uix_guild_embed_key'),
    )

    # No ALTER TABLE calls needed — tables were created with their final types above


def downgrade() -> None:
    """Downgrade schema — drop all tables."""
    op.drop_table('embed_config')
    op.drop_table('guild_config')
    op.drop_table('nuclear_logs')
    op.drop_table('nuclear_data')
    op.drop_table('user_data')
