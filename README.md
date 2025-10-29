# Dashboard FIFA - Análisis Comparativo por Clubes y Jugadores

Este repositorio contiene un dashboard realizado en Power BI para analizar los datos oficiales de FIFA desde 2017 a 2022.  
El objetivo es comparar el rendimiento de clubes y jugadores a lo largo de diferentes años.

## 📊 Contenido

- **Dashboard FIFA.pbix**: Dashboard interactivo en Power BI (13 MB)
- **FIFA17_official_data.csv** a **FIFA22_official_data.csv**: Datasets utilizados para el análisis (~7 MB cada uno)

### Especificaciones de los Datos

| Archivo | Filas | Columnas | Tamaño | Codificación |
|---------|-------|----------|--------|--------------|
| FIFA17_official_data.csv | 17,622 | 64 | 7.36 MB | UTF-8 |
| FIFA18_official_data.csv | 17,927 | 65 | 6.20 MB | UTF-8 |
| FIFA19_official_data.csv | 18,006 | 65 | 7.65 MB | UTF-8 |
| FIFA20_official_data.csv | 17,154 | 66 | 7.54 MB | UTF-8 |
| FIFA21_official_data.csv | 17,170 | 66 | 7.11 MB | UTF-8 |
| FIFA22_official_data.csv | 16,710 | 67 | 7.09 MB | UTF-8 |

**Total de datos**: ~104,000 registros de jugadores a través de 6 temporadas

## 🎯 Descripción del Análisis

- **Comparativa de clubes por año**: Análisis del rendimiento y evolución de los clubes de fútbol
- **Evolución de jugadores**: Seguimiento de estadísticas, habilidades y rendimiento individual
- **Visualizaciones avanzadas**: Identificación de tendencias y cambios en equipos y jugadores
- **Filtros interactivos**: Exploración por temporada, club, jugador, nacionalidad y más

## 🚀 Cómo Usar

1. **Requisitos**: Microsoft Power BI Desktop (versión recomendada: última)
2. **Abrir el Dashboard**: Doble clic en `Dashboard FIFA.pbix`
3. **Cargar datos**: Los archivos CSV están vinculados automáticamente
4. **Explorar**: Utiliza los filtros y visualizaciones interactivas

## 📁 Estructura de Datos CSV

Los archivos CSV contienen información detallada de cada jugador:

- **Información básica**: ID, Nombre, Edad, Nacionalidad, Club
- **Atributos físicos**: Altura, Peso, Pie preferido
- **Estadísticas de juego**: Overall, Potencial, Posición
- **Habilidades técnicas**: Dribbling, Pase, Tiro, Defensa, etc.
- **Información del contrato**: Valor de mercado, Salario, Fecha de contrato
- **Habilidades específicas de portero**: GK Diving, Handling, Reflexes, etc.

### Formato de Archivos

- **Delimitador**: Coma (`,`)
- **Codificación**: UTF-8
- **Primera fila**: Encabezados de columna
- **Valores faltantes**: Representados como `nan` o celdas vacías

## 🔧 Optimizaciones Realizadas

- ✅ Estandarización de delimitadores CSV (todos usan coma)
- ✅ Codificación UTF-8 consistente en todos los archivos
- ✅ Eliminación de BOM (Byte Order Mark) innecesarios
- ✅ Normalización de espacios en blanco
- ✅ Documentación mejorada con especificaciones técnicas

## 📝 Notas Técnicas

- Los datos están optimizados para carga rápida en Power BI
- Se recomienda no modificar la estructura de las columnas para mantener compatibilidad con el dashboard
- Los archivos CSV pueden ser abiertos con Excel, Python (pandas), R, u otras herramientas de análisis

## 🤝 Contribuciones

Si deseas contribuir con mejoras al dashboard o encontrar errores, por favor abre un issue o pull request.

## 📄 Licencia

Los datos son de dominio público de EA Sports FIFA. El dashboard y visualizaciones son de uso educativo y análisis.
