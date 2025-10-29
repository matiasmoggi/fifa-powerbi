# Dashboard FIFA - Análisis Comparativo por Clubes y Jugadores

Este repositorio contiene un dashboard realizado en Power BI para analizar los datos oficiales de FIFA desde 2017 a 2022.  
El objetivo es comparar el rendimiento de clubes y jugadores a lo largo de diferentes años.

## Contenido

- **Dashboard FIFA.pbix**: Dashboard interactivo en Power BI.
- **FIFA17_official_data.csv** a **FIFA22_official_data.csv**: Datasets originales utilizados para el análisis.
- **optimize_data.py**: Script de optimización para mejorar el rendimiento (RECOMENDADO).
- **PERFORMANCE_GUIDE.md**: Guía completa de optimización de rendimiento.

## Descripción del análisis

- Comparativa de clubes por año.
- Comparativa y evolución de jugadores (estadísticas, rendimiento, etc.).
- Visualizaciones para identificar tendencias y cambios en los equipos y jugadores.
- Filtros para explorar los datos por temporada, club y jugador.

## ⚡ Optimización de Rendimiento

### Mejoras Implementadas

Se han identificado y solucionado varios problemas de rendimiento:

1. **Problemas de codificación**: Los archivos CSV utilizan codificaciones mixtas (ISO-8859-1, MacRoman)
2. **Datos duplicados**: Los mismos jugadores se almacenan en 6 archivos diferentes (factor de duplicación 2.25x)
3. **Columnas URL redundantes**: Las columnas Photo, Flag y Club Logo ocupan ~4-5 MB innecesarios
4. **Estructura no normalizada**: Datos denormalizados que afectan el rendimiento

### Cómo Optimizar

Para mejorar significativamente el rendimiento del dashboard:

```bash
# Instalar dependencia (si es necesario)
pip install chardet

# Ejecutar script de optimización
python3 optimize_data.py
```

**Resultados esperados:**
- ✅ Reducción de tamaño: 42.51 MB → 23.61 MB (44.5% menos)
- ✅ Tiempo de carga: ~50% más rápido
- ✅ Modelo de datos más limpio y mantenible
- ✅ Archivos consolidados con corrección de codificación

### Archivos Generados

Después de ejecutar la optimización:
- `fifa_data_consolidated.csv`: Archivo consolidado con todos los años (incluye columna Year)
- `dimension_tables/dim_clubs.csv`: Tabla de dimensión de clubes (1,040 clubes únicos)
- `dimension_tables/dim_nationalities.csv`: Tabla de dimensión de nacionalidades (194 nacionalidades)

### Uso en Power BI

1. Importa `fifa_data_consolidated.csv` en lugar de los 6 archivos individuales
2. Importa las tablas de dimensión desde `dimension_tables/`
3. Crea relaciones entre las tablas de hechos y dimensión
4. Elimina las fuentes de datos antiguas del modelo
5. Actualiza el modelo de datos y verifica las consultas

Para más detalles, consulta **[PERFORMANCE_GUIDE.md](PERFORMANCE_GUIDE.md)**

## Validación

Valida que la optimización fue exitosa:

```bash
python3 validate_optimization.py
```
