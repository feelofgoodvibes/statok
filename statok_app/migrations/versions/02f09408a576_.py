"""Test data

Revision ID: 02f09408a576
Revises: baabe4b7303f
Create Date: 2023-03-06 02:35:31.331857

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02f09408a576'
down_revision = 'baabe4b7303f'
branch_labels = None
depends_on = None


def upgrade():
    # Income categories
    op.execute("INSERT INTO category VALUES (3, 'Salary', 'INCOME')")
    op.execute("INSERT INTO category VALUES (4, 'Pocket money', 'INCOME')")

    # Expense categories
    op.execute("INSERT INTO category VALUES (5, 'Entertainment', 'EXPENSE')")
    op.execute("INSERT INTO category VALUES (6, 'Shopping', 'EXPENSE')")
    op.execute("INSERT INTO category VALUES (7, 'Food', 'EXPENSE')")
    op.execute("INSERT INTO category VALUES (8, 'Clothing', 'EXPENSE')")
    op.execute("INSERT INTO category VALUES (9, 'Health', 'EXPENSE')")

    # Operations
    op.execute("INSERT INTO operation VALUES (1, 2000, '2023-02-01 15:00:00', 3)")
    op.execute("INSERT INTO operation VALUES (2, -12.56, '2023-02-01 16:18:12', 7)")
    op.execute("INSERT INTO operation VALUES (3, -135, '2023-02-01 16:55:13', 8)")
    op.execute("INSERT INTO operation VALUES (4, -5.45, '2023-02-01 16:55:13', 9)")

    op.execute("INSERT INTO operation VALUES (5, -13.5, '2023-02-02 10:02:10', 9)")
    op.execute("INSERT INTO operation VALUES (6, -26.88, '2023-02-02 13:46:05', 6)")
    op.execute("INSERT INTO operation VALUES (7, 139, '2023-02-02 15:12:00', 1)")
    op.execute("INSERT INTO operation VALUES (8, 250, '2023-02-02 16:20:06', 1)")
    op.execute("INSERT INTO operation VALUES (9, -62.25, '2023-02-02 18:02:12', 7)")
    op.execute("INSERT INTO operation VALUES (10, -13.56, '2023-02-02 18:25:06', 6)")
    op.execute("INSERT INTO operation VALUES (11, -26.8, '2023-02-02 18:33:46', 6)")
    op.execute("INSERT INTO operation VALUES (12, -35.89, '2023-02-02 18:39:55', 6)")

    op.execute("INSERT INTO operation VALUES (13, -12.00, '2023-02-03 10:05:12', 7)")
    op.execute("INSERT INTO operation VALUES (14, -5.00, '2023-02-03 13:05:13', 9)")
    op.execute("INSERT INTO operation VALUES (15, -1.23, '2023-02-03 21:13:50', 5)")

    op.execute("INSERT INTO operation VALUES (16, -120.13, '2023-02-04 13:00:15', 8)")
    op.execute("INSERT INTO operation VALUES (17, -6.89, '2023-02-04 23:15:10', 6)")

    op.execute("INSERT INTO operation VALUES (18, -240.00, '2023-02-05 09:12:18', 5)")

    op.execute("INSERT INTO operation VALUES (19, 500.00, '2023-02-10 08:00:00', 3)")
    op.execute("INSERT INTO operation VALUES (20, -260.50, '2023-02-10 16:43:19', 8)")
    op.execute("INSERT INTO operation VALUES (21, -125.12, '2023-02-10 21:02:15', 6)")


def downgrade():
    op.execute("SET FOREIGN_KEY_CHECKS = 0;")
    op.execute("TRUNCATE operation")
    op.execute("TRUNCATE category")
    op.execute("SET FOREIGN_KEY_CHECKS = 1;")
    op.execute("INSERT INTO category VALUES (1, 'Other', 'INCOME')")
    op.execute("INSERT INTO category VALUES (2, 'Other', 'EXPENSE')")
