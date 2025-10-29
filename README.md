# Dashboard FIFA - Análisis Comparativo por Clubes y Jugadores

Este repositorio contiene un dashboard realizado en Power BI para analizar los datos oficiales de FIFA desde 2017 a 2022.  
El objetivo es comparar el rendimiento de clubes y jugadores a lo largo de diferentes años.

## Contenido

- **Dashboard FIFA.pbix**: Dashboard interactivo en Power BI.
- **FIFA17_official_data.csv** a **FIFA22_official_data.csv**: Datasets utilizados para el análisis.
- **optimize_data.py**: Script de optimización para mejorar la calidad y rendimiento de los datos.
- **PERFORMANCE_IMPROVEMENTS.md**: Documentación detallada sobre mejoras de rendimiento y calidad de datos.

## Descripción del análisis

- Comparativa de clubes por año.
- Comparativa y evolución de jugadores (estadísticas, rendimiento, etc.).
- Visualizaciones para identificar tendencias y cambios en los equipos y jugadores.
- Filtros para explorar los datos por temporada, club y jugador.

## Optimización de datos

Para mejorar el rendimiento y la calidad de los datos, se ha incluido un script de optimización que:

- Estandariza la codificación de caracteres (UTF-8)
- Corrige problemas de codificación en nombres y caracteres especiales
- Estandariza delimitadores a coma (,)
- Estandariza finales de línea
- Elimina etiquetas HTML de los datos
- Opcionalmente elimina columnas de URLs para reducir el tamaño de los archivos

### Uso del script de optimización

```bash
# Optimización básica (conserva URLs)
python3 optimize_data.py --backup

# Optimización completa (elimina URLs para reducir tamaño)
python3 optimize_data.py --remove-urls --backup
```

**Nota**: Se recomienda usar la opción `--backup` para crear copias de seguridad de los archivos originales.

### Mejoras de rendimiento

Consulta [PERFORMANCE_IMPROVEMENTS.md](PERFORMANCE_IMPROVEMENTS.md) para información detallada sobre:
- Problemas de rendimiento identificados
- Recomendaciones de optimización
- Resultados esperados
- Plan de implementación por fases
