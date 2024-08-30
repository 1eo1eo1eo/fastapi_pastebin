"""update users(add registrated_at), create messages table

Revision ID: 9843d8876652
Revises: 2d1e8021ffd4
Create Date: 2024-08-30 11:51:33.647418

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9843d8876652"
down_revision: Union[str, None] = "2d1e8021ffd4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "messages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=50), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("language", sa.String(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=False),
        sa.Column("sid", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["sid"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column("users", sa.Column("registered_at", sa.TIMESTAMP(), nullable=False))


def downgrade() -> None:
    op.drop_column("users", "registered_at")
    op.drop_table("messages")
