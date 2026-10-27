# Modelo entidad relación · ejemplo

```mermaid
erDiagram
    CASOS ||--o{ EVENTOS : registra
    CASOS {
        int id PK
        varchar radicado
        varchar escenario
        varchar bpmn_id
        varchar instance_key
        double area_terreno_m2
        double area_construida_m2
        varchar uso
        varchar chip
        bool validacion_previa_ok
        double valor_referencia_demo
        varchar estado
        timestamp creado_en
        timestamp cerrado_en
    }
    EVENTOS {
        int id PK
        int caso_id FK
        timestamp momento
        varchar accion
        varchar tarea
        varchar actor
        text detalles
    }
```

`Caso` representa un expediente simplificado e instancia BPMN. `Evento` registra acciones auditables; almacena los detalles como JSON serializado para que el ejemplo funcione en SQLite y PostgreSQL sin migración compleja.

**Para trabajo autónomo:** ampliar `documentos`, `actividades`, `observaciones`, `reglas`, `kpi_snapshot`, `usuarios/roles` sólo después de agregar requisitos EARS y pruebas. Evitar inventar tablas que no sean necesarias en el vertical slice.

Modelo gestionado por SQLAlchemy (`app/db.py`). Vista SQL `vw_preset_casos` creada automáticamente en el arranque.
