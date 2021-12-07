"""added new filed

Revision ID: 8006fdb10621
Revises: a5f6ea9ad79a
Create Date: 2021-11-29 23:18:35.227201

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8006fdb10621'
down_revision = 'a5f6ea9ad79a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('films', sa.Column('test', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('films', 'test')
    # ### end Alembic commands ###