# Extractor de datos de diferentes plataformas 

La idea es poder extraer datos de plataformas digitales y acumularlos en una base de datos. Plataformas soportadas: tiktok.

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

Por defecto sólo se obtienen datos de videos con una antigüedad máxma de 120 días y los 20 últimos posts del perfil.

## Licencia

Este software esta bajo licencia GPLv3. Es libre y debe mantenerse así ver [LICENSE.md](LICENSE.md)



