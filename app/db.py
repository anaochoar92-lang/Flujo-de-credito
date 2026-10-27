import os
from datetime import datetime, timezone
from sqlalchemy import String, Float, Integer, Boolean, DateTime, ForeignKey, Text, create_engine, text, inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.engine import URL

class Base(DeclarativeBase):
    pass

class Caso(Base):
    __tablename__ = "casos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    radicado: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    escenario: Mapped[str] = mapped_column(String(8), nullable=False)
    bpmn_id: Mapped[str] = mapped_column(String(100), nullable=False)
    instance_key: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
    area_terreno_m2: Mapped[float] = mapped_column(Float)
    area_construida_m2: Mapped[float] = mapped_column(Float)
    uso: Mapped[str] = mapped_column(String(50))
    chip: Mapped[str | None] = mapped_column(String(50), nullable=True)
    validacion_previa_ok: Mapped[bool] = mapped_column(Boolean, default=True)
    valor_referencia_demo: Mapped[float] = mapped_column(Float, default=0)
    estado: Mapped[str] = mapped_column(String(30), default="EN_PROCESO")
    etapa_mock: Mapped[int] = mapped_column(Integer, default=0)
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    cerrado_en: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    events: Mapped[list["Evento"]] = relationship(back_populates="caso", cascade="all, delete-orphan")

class Evento(Base):
    __tablename__ = "eventos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    caso_id: Mapped[int] = mapped_column(ForeignKey("casos.id"), nullable=False, index=True)
    momento: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    accion: Mapped[str] = mapped_column(String(90))
    tarea: Mapped[str | None] = mapped_column(String(120), nullable=True)
    actor: Mapped[str] = mapped_column(String(80), default="estudiante")
    detalles: Mapped[str] = mapped_column(Text, default="{}")
    caso: Mapped[Caso] = relationship(back_populates="events")

engine = None
Session = None

def setup_db(url: str | None = None):
    global engine, Session
    if url is None:
        url = os.getenv("DATABASE_URL")
    if not url and os.getenv("DB_HOST"):
        url = URL.create("postgresql+psycopg", username=os.getenv("DB_USER", "mba"),
                         password=os.getenv("DB_PASSWORD", ""),host=os.getenv("DB_HOST"),
                         port=int(os.getenv("DB_PORT", "5432")),database=os.getenv("DB_NAME", "mba_mvp"))
    if not url:
        url = "sqlite:///./mvp.sqlite3"
    connect_args = {"check_same_thread": False} if str(url).startswith("sqlite") else {}
    kwargs = {"connect_args": connect_args, "pool_pre_ping": True}
    if url == "sqlite://":
        kwargs["poolclass"] = StaticPool
    engine = create_engine(url, **kwargs)
    Session = sessionmaker(engine, expire_on_commit=False)
    Base.metadata.create_all(engine)
    if "vw_preset_casos" not in inspect(engine).get_view_names():
        with engine.begin() as conn:
            conn.execute(text("""CREATE VIEW vw_preset_casos AS
              SELECT id, radicado, escenario, estado, area_terreno_m2, area_construida_m2,
                     valor_referencia_demo, validacion_previa_ok, creado_en, cerrado_en
              FROM casos"""))
    return Session
