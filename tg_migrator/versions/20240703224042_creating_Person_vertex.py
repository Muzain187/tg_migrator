"""Migration: creating Person vertex"""
                       
"""
version id: versions/20240703224042_creating_Person_vertex.py 
"""

def upgrade():
    ddl_upgrade = """
    DROP JOB tg_migrator_upgrade_20240703224042
    CREATE  SCHEMA_CHANGE JOB tg_migrator_upgrade_20240703224042 {
        ADD VERTEX Person(PRIMARY_ID id STRING,name STRING) WITH primary_id_as_attribute="true";
        
    }
    RUN SCHEMA_CHANGE JOB tg_migrator_upgrade_20240703224042
    """
    return ddl_upgrade

def downgrade():
    ddl_downgrade = """
    DROP JOB tg_migrator_downgrade_20240703224042
    CREATE  SCHEMA_CHANGE JOB tg_migrator_downgrade_20240703224042  {
        DROP VERTEX Person;
    }
    RUN SCHEMA_CHANGE JOB tg_migrator_downgrade_20240703224042 
    """
    return ddl_downgrade
                
                
                