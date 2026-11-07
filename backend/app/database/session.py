from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.database.models import Base

engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    # Automatic schema migration for existing SQLite tables
    try:
        with engine.connect() as conn:
            result = conn.execute(text("PRAGMA table_info(analysis_results)"))
            existing_cols = {row[1] for row in result.fetchall()}
            if existing_cols:
                cols_to_add = {
                    "detection_mode": "VARCHAR(30) DEFAULT 'RULE_ONLY'",
                    "ml_predicted_class": "VARCHAR(30)",
                    "ml_confidence": "FLOAT",
                    "ml_model_version": "VARCHAR(100)",
                    "rule_score": "FLOAT",
                    "ml_score": "FLOAT",
                }
                for col_name, col_def in cols_to_add.items():
                    if col_name not in existing_cols:
                        conn.execute(text(f"ALTER TABLE analysis_results ADD COLUMN {col_name} {col_def}"))
                conn.commit()
    except Exception:
        pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
