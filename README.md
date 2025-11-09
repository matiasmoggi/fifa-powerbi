# Dashboard FIFA - Análisis Comparativo por Clubes y Jugadores

Este repositorio contiene un dashboard realizado en Power BI para analizar los datos oficiales de FIFA desde 2017 a 2022.  
El objetivo es comparar el rendimiento de clubes y jugadores a lo largo de diferentes años.

## Contenido

- **Dashboard FIFA.pbix**: Dashboard interactivo en Power BI.
- **FIFA17_official_data.csv** a **FIFA22_official_data.csv**: Datasets utilizados para el análisis.

## Descripción del análisis

- Comparativa de clubes por año.
- Comparativa y evolución de jugadores (estadísticas, rendimiento, etc.).
- Visualizaciones para identificar tendencias y cambios en los equipos y jugadores.
- Filtros para explorar los datos por temporada, club y jugador.

## 📦 Manejo de archivos grandes / Large Files Handling

### Español

Este repositorio utiliza **Git LFS (Large File Storage)** para manejar archivos grandes como el archivo de Power BI (.pbix) y los datasets (.csv).

#### ¿Qué es Git LFS?

Git LFS es una extensión de Git que permite manejar archivos grandes de manera eficiente. En lugar de almacenar los archivos completos en el repositorio, Git LFS almacena referencias pequeñas mientras que los archivos reales se guardan en un servidor separado.

#### ¿Cómo clonar este repositorio?

Si quieres clonar este repositorio y descargar todos los archivos grandes:

1. **Instala Git LFS** (si aún no lo tienes):
   ```bash
   # En Ubuntu/Debian
   sudo apt-get install git-lfs
   
   # En macOS
   brew install git-lfs
   
   # En Windows: Descarga desde https://git-lfs.github.com/
   ```

2. **Inicializa Git LFS**:
   ```bash
   git lfs install
   ```

3. **Clona el repositorio**:
   ```bash
   git clone https://github.com/matiasmoggi/fifa-powerbi.git
   cd fifa-powerbi
   ```

Los archivos grandes se descargarán automáticamente.

#### ¿Cómo subir archivos grandes?

Si necesitas actualizar o agregar archivos grandes:

1. Asegúrate de tener Git LFS instalado e inicializado
2. Los archivos .pbix y .csv ya están configurados para usar Git LFS automáticamente
3. Simplemente agrega y confirma tus cambios como de costumbre:
   ```bash
   git add "Dashboard FIFA.pbix"
   git commit -m "Actualizar dashboard"
   git push
   ```

#### Solución al error "File is too large" (Archivo muy grande)

Si recibes el error **"Yowza, that's a big file. Try again with a file smaller than 25MB"**, es porque estás intentando subir un archivo grande sin Git LFS. Sigue estos pasos:

1. Instala e inicializa Git LFS (ver arriba)
2. Asegúrate de que el archivo `.gitattributes` existe en el repositorio
3. Si ya agregaste el archivo al repositorio sin LFS, necesitas migrarlo:
   ```bash
   git lfs migrate import --include="*.pbix,*.csv" --everything
   ```
4. Empuja los cambios:
   ```bash
   git push origin --force --all
   ```

### English

This repository uses **Git LFS (Large File Storage)** to handle large files such as Power BI files (.pbix) and datasets (.csv).

#### What is Git LFS?

Git LFS is a Git extension that allows efficient handling of large files. Instead of storing complete files in the repository, Git LFS stores small references while the actual files are saved on a separate server.

#### How to clone this repository?

If you want to clone this repository and download all large files:

1. **Install Git LFS** (if you don't have it yet):
   ```bash
   # On Ubuntu/Debian
   sudo apt-get install git-lfs
   
   # On macOS
   brew install git-lfs
   
   # On Windows: Download from https://git-lfs.github.com/
   ```

2. **Initialize Git LFS**:
   ```bash
   git lfs install
   ```

3. **Clone the repository**:
   ```bash
   git clone https://github.com/matiasmoggi/fifa-powerbi.git
   cd fifa-powerbi
   ```

Large files will be downloaded automatically.

#### How to upload large files?

If you need to update or add large files:

1. Make sure you have Git LFS installed and initialized
2. .pbix and .csv files are already configured to use Git LFS automatically
3. Simply add and commit your changes as usual:
   ```bash
   git add "Dashboard FIFA.pbix"
   git commit -m "Update dashboard"
   git push
   ```

#### Solution for "File is too large" error

If you receive the error **"Yowza, that's a big file. Try again with a file smaller than 25MB"**, it's because you're trying to upload a large file without Git LFS. Follow these steps:

1. Install and initialize Git LFS (see above)
2. Make sure the `.gitattributes` file exists in the repository
3. If you already added the file to the repository without LFS, you need to migrate it:
   ```bash
   git lfs migrate import --include="*.pbix,*.csv" --everything
   ```
4. Push the changes:
   ```bash
   git push origin --force --all
   ```
