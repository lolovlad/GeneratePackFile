"""empty message

Revision ID: d6467550e353
Revises: 3c1a34fb155d
Create Date: 2024-04-18 19:09:47.454294

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd6467550e353'
down_revision: Union[str, None] = '3c1a34fb155d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('organizations_to_user')
    op.add_column('organizations', sa.Column('id_user', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'organizations', 'user', ['id_user'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'organizations', type_='foreignkey')
    op.drop_column('organizations', 'id_user')
    op.create_table('organizations_to_user',
    sa.Column('id_user', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('id_organization', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['id_organization'], ['organizations.id'], name='organizations_to_user_id_organization_fkey'),
    sa.ForeignKeyConstraint(['id_user'], ['user.id'], name='organizations_to_user_id_user_fkey'),
    sa.PrimaryKeyConstraint('id_user', 'id_organization', name='organizations_to_user_pkey')
    )
    # ### end Alembic commands ###
