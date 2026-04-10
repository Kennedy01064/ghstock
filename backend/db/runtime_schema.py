from sqlalchemy import inspect

from backend import models
from backend.db.session import Base, engine


def ensure_runtime_schema() -> None:
    """Create missing operational tables/columns required by the current backend."""
    Base.metadata.create_all(bind=engine)
    inspector = inspect(engine)

    if inspector.has_table("user"):
        user_columns = {column["name"] for column in inspector.get_columns("user")}
    else:
        user_columns = set()

    if inspector.has_table("system_setting"):
        system_setting_columns = {
            column["name"] for column in inspector.get_columns("system_setting")
        }
    else:
        system_setting_columns = set()

    with engine.begin() as connection:
        if "is_active" not in user_columns:
            default_literal = "1" if engine.dialect.name == "sqlite" else "TRUE"
            connection.exec_driver_sql(
                f'ALTER TABLE "user" ADD COLUMN is_active BOOLEAN DEFAULT {default_literal}'
            )

        for table in (models.SystemSetting.__table__, models.AuditLog.__table__):
            if not inspector.has_table(table.name):
                table.create(bind=connection)

        if "order_submission_deadline_at" not in system_setting_columns:
            connection.exec_driver_sql(
                'ALTER TABLE "system_setting" ADD COLUMN order_submission_deadline_at DATETIME'
            )

        if "order_submission_deadline_note" not in system_setting_columns:
            connection.exec_driver_sql(
                'ALTER TABLE "system_setting" ADD COLUMN order_submission_deadline_note TEXT'
            )

        if inspector.has_table("user"):
            active_literal = "1" if engine.dialect.name == "sqlite" else "TRUE"
            connection.exec_driver_sql(
                f'UPDATE "user" SET is_active = {active_literal} WHERE is_active IS NULL'
            )
