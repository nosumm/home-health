"""packets table

Revision ID: 271da97d81f5
Revises: 48f96743af08
Create Date: 2022-02-16 15:19:38.278887

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '271da97d81f5'
down_revision = '48f96743af08'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('packet', sa.Column('test_type', sa.String(length=40), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('packet', 'test_type')
    # ### end Alembic commands ###
