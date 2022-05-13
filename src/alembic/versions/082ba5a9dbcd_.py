"""empty message

Revision ID: 082ba5a9dbcd
Revises: 3d4234e7f162
Create Date: 2022-05-14 00:16:37.349069

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '082ba5a9dbcd'
down_revision = '3d4234e7f162'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('author',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=100), nullable=False),
                    sa.Column('description', sa.String(length=255), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('tag',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=100), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('author_elective',
                    sa.Column('elective_id', sa.Integer(), nullable=True),
                    sa.Column('author_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(tuple(['author_id']), ['author.id'], ),
                    sa.ForeignKeyConstraint(tuple(['elective_id']), ['elective.id'], )
                    )
    op.create_table('tag_elective',
                    sa.Column('elective_id', sa.Integer(), nullable=True),
                    sa.Column('tag_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(tuple(['elective_id']), ['elective.id'], ),
                    sa.ForeignKeyConstraint(tuple(['tag_id']), ['tag.id'], )
                    )
    op.alter_column('elective', 'title',
                    existing_type=sa.VARCHAR(length=50),
                    nullable=False)
    op.alter_column('elective', 'short_description',
                    existing_type=sa.VARCHAR(length=50),
                    nullable=False)
    op.alter_column('elective', 'full_description',
                    existing_type=sa.VARCHAR(length=255),
                    nullable=False)
    op.alter_column('minor', 'title',
                    existing_type=sa.VARCHAR(length=255),
                    nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('minor', 'title',
                    existing_type=sa.VARCHAR(length=255),
                    nullable=True)
    op.alter_column('elective', 'full_description',
                    existing_type=sa.VARCHAR(length=255),
                    nullable=True)
    op.alter_column('elective', 'short_description',
                    existing_type=sa.VARCHAR(length=50),
                    nullable=True)
    op.alter_column('elective', 'title',
                    existing_type=sa.VARCHAR(length=50),
                    nullable=True)
    op.drop_table('tag_elective')
    op.drop_table('author_elective')
    op.drop_table('tag')
    op.drop_table('author')
    # ### end Alembic commands ###
