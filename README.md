# Extractor de datos de diferentes plataformas 

La idea es poder extraer datos de plataformas digitales y acumularlos en una base de datos. Plataformas soportadas: tiktok, facebook.

## Instalación

Se puede hacer con `pipenv`.

1. Crear entorno virtual `pipenv shell`
2. Instalar paquetes `pipenv install`

### Base de datos

Se usa postgresql como gestor de base de datos ([esquema](doc/db_schema.jpg)). Se necesita primero tener la BD creada.

1. Crear la BD (nombre por defecto socialmedia1)
2. Ejecutar el script de creación en `src/db/createDb.sql`
3. Modificar el archivo `src/db/db_manager.py` la función `create_engine` para especificar `user, password, host, database` como sea necesario.

## tiktok

Usa playwright para hacer scraping y obtener datos de perfiles dados, el archivo con las cuentas está en `data/tiktokProfiles.sample.csv`.

Para ejecutar: 

```bash
python tiktok_profiles.py --from_file=./data/tiktokProfiles.sample.csv --only_metadata
```

Por defecto sólo se obtienen datos de videos con una antigüedad máxma de 120 días y los 7 últimos posts del perfil.

## facebook

Hace scraping con playwright, toma en cuenta los perfiles en archivos csv dentro el directorio `data/facebook`. Toma en cuenta archivos con columnas:

- "Nombre": Nombre del perfil
- "Facebook": URL del perfil.

Para ejecutar:

```bash
# Si es la primera vez que se ejecuta hay que hacer login manualmente
# Luego de hacer login pasado unos segundos se comienza con el barrido de cuentas
python facebook_profiles.py --login 

# Una vez que se hizo login las siguientes ejecuciones son con
python facebook_profiles.py
```

## reportes desde la BD

```bash
python reports.py
```

## Licencia

Este software esta bajo licencia GPLv3. Es libre y debe mantenerse así ver [LICENSE.md](LICENSE.md)



