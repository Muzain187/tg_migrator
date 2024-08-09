"""Migration: creating freind edge"""
                       
"""
version id: versions/20240703224218_creating_location.py 
"""

def upgrade():
    ddl_upgrade = """
    DROP JOB tg_migrator_upgrade_20240703224218
    CREATE  SCHEMA_CHANGE JOB tg_migrator_upgrade_20240703224218 {
        ADD VERTEX Location(PRIMARY_ID id STRING,lat FLOAT,lng FLOAT) WITH primary_id_as_attribute="true";
    }
    RUN SCHEMA_CHANGE JOB tg_migrator_upgrade_20240703224218
    """
    return ddl_upgrade

def downgrade():
    ddl_downgrade = """
    DROP JOB tg_migrator_downgrade_20240703224218
    CREATE  SCHEMA_CHANGE JOB tg_migrator_downgrade_20240703224218  {
        DROP VERTEX Location;
    }
    RUN SCHEMA_CHANGE JOB tg_migrator_downgrade_20240703224218
    """
    return ddl_downgrade
                
                
                