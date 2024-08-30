"""fix messages table(sid column)

Revision ID: f765d92546f0
Revises: ca3914bd33e3
Create Date: 2024-08-30 13:26:43.420431

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f765d92546f0"
down_revision: Union[str, None] = "ca3914bd33e3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("messages_sid_fkey", "messages", type_="foreignkey")
    op.alter_column(
        "messages",
        "sid",
        existing_type=sa.INTEGER(),
        type_=sa.String(),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.create_foreign_key("messages_sid_fkey", "messages", "users", ["sid"], ["id"])
    op.alter_column(
        "messages",
        "sid",
        existing_type=sa.String(),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
