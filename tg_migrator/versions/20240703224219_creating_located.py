"""Migration: creating located edge"""
                       
"""
version id: versions/20240703224219_creating_located_edge.py 
"""

def upgrade():
    ddl_upgrade = """
    DROP JOB tg_migrator_upgrade_20240703224219
    CREATE  SCHEMA_CHANGE JOB tg_migrator_upgrade_20240703224219 {
        ADD DIRECTED EDGE located (FROM Person, TO Location);
    }
    RUN SCHEMA_CHANGE JOB tg_migrator_upgrade_20240703224219
    """
    return ddl_upgrade

def downgrade():
    ddl_downgrade = """
    DROP JOB tg_migrator_downgrade_20240703224219
    CREATE  SCHEMA_CHANGE JOB tg_migrator_downgrade_20240703224219  {
        DROP EDGE located;
    }
    RUN SCHEMA_CHANGE JOB tg_migrator_downgrade_20240703224219 
    """
    return ddl_downgrade
                
                
                