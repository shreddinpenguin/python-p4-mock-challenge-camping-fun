"""implement relationships

Revision ID: e9e75df8d416
Revises: d6f1f6e38f8c
Create Date: 2023-11-20 09:58:41.701730

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9e75df8d416'
down_revision = 'd6f1f6e38f8c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('signups', sa.Column('camper_id', sa.Integer(), nullable=True))
    op.add_column('signups', sa.Column('activity_id', sa.Integer(), nullable=True))
    op.create_foreign_key(op.f('fk_signups_camper_id_campers'), 'signups', 'campers', ['camper_id'], ['id'])
    op.create_foreign_key(op.f('fk_signups_activity_id_activities'), 'signups', 'activities', ['activity_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_signups_activity_id_activities'), 'signups', type_='foreignkey')
    op.drop_constraint(op.f('fk_signups_camper_id_campers'), 'signups', type_='foreignkey')
    op.drop_column('signups', 'activity_id')
    op.drop_column('signups', 'camper_id')
    # ### end Alembic commands ###
