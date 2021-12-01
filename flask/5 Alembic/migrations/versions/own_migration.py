"""added new filed

Revision ID: 8006fdb10621
Revises: a5f6ea9ad79a
Create Date: 2021-11-29 23:22:35.227201

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import text

revision = '8006fdb10622'
down_revision = '8006fdb10621'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute(
        text(
            """
            UPDATE films
            SET test = 100
            WHERE title like '%Deathly%'
            """
        )
    )


def downgrade():
    conn = op.get_bind()
    conn.execute(
        text(
            """
            UPDATE films
            SET test = NULL
            WHERE title like '%Deathly%'
            """
        )
    )