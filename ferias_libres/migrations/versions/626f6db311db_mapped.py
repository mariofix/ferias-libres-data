"""Mapped

Revision ID: 626f6db311db
Revises: acc25e8c5fba
Create Date: 2023-07-05 03:23:25.433889

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "626f6db311db"
down_revision = "acc25e8c5fba"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("ferias_feria", schema=None) as batch_op:
        batch_op.add_column(sa.Column("dias", sa.JSON(), nullable=False))
        batch_op.alter_column("slug", existing_type=mysql.VARCHAR(length=64), nullable=False)
        batch_op.alter_column("nombre", existing_type=mysql.VARCHAR(length=64), nullable=False)
        batch_op.alter_column(
            "ubicacion", existing_type=mysql.LONGTEXT(charset="utf8mb4", collation="utf8mb4_bin"), nullable=False
        )
        batch_op.drop_column("sabado")
        batch_op.drop_column("jueves")
        batch_op.drop_column("lunes")
        batch_op.drop_column("viernes")
        batch_op.drop_column("miercoles")
        batch_op.drop_column("domingo")
        batch_op.drop_column("martes")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("ferias_feria", schema=None) as batch_op:
        batch_op.add_column(sa.Column("martes", mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column("domingo", mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column("miercoles", mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column("viernes", mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column("lunes", mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column("jueves", mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column("sabado", mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
        batch_op.alter_column(
            "ubicacion", existing_type=mysql.LONGTEXT(charset="utf8mb4", collation="utf8mb4_bin"), nullable=True
        )
        batch_op.alter_column("nombre", existing_type=mysql.VARCHAR(length=64), nullable=True)
        batch_op.alter_column("slug", existing_type=mysql.VARCHAR(length=64), nullable=True)
        batch_op.drop_column("dias")

    # ### end Alembic commands ###
