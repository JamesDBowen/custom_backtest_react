"""empty message

Revision ID: e0feeead509
Revises: 31e1d9758bdf
Create Date: 2017-05-11 10:54:40.812450

"""

# revision identifiers, used by Alembic.
revision = 'e0feeead509'
down_revision = '31e1d9758bdf'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('series', sa.Column('custom', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('series', 'custom')
    ### end Alembic commands ###
