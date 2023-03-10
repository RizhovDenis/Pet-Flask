"""change avatar type

Revision ID: 43576bf87fbf
Revises: 3b368e2d12e2
Create Date: 2022-10-24 13:44:56.792094

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '43576bf87fbf'
down_revision = '3b368e2d12e2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'avatar')
    op.add_column('users', sa.Column(
        'avatar', sa.String(), nullable=True))
    op.create_unique_constraint(None, 'users', ['avatar'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
