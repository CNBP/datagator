"""added two new fields about me and last seen for User class

Revision ID: 545c2820d717
Revises: 8669596286b2
Create Date: 2019-09-18 11:36:18.381015

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "545c2820d717"
down_revision = "8669596286b2"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "entry",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("MRN", sa.Integer(), nullable=True),
        sa.Column("CNBPID", sa.String(length=10), nullable=True),
        sa.Column("birth_weight", sa.String(length=140), nullable=True),
        sa.Column("birth_date", sa.Date(), nullable=True),
        sa.Column("birth_time", sa.Time(), nullable=True),
        sa.Column("mri_date", sa.Date(), nullable=True),
        sa.Column("mri_reason", sa.String(), nullable=True),
        sa.Column("mri_dx", sa.String(), nullable=True),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_entry_timestamp"), "entry", ["timestamp"], unique=False)
    op.add_column("user", sa.Column("about_me", sa.String(length=140), nullable=True))
    op.add_column("user", sa.Column("last_seen", sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "last_seen")
    op.drop_column("user", "about_me")
    op.drop_index(op.f("ix_entry_timestamp"), table_name="entry")
    op.drop_table("entry")
    # ### end Alembic commands ###