"""Migration: creating freind edge"""
                       
"""
version id: versions/20240703224217_creating_freind_edge.py 
"""

def upgrade():
    ddl_upgrade = """
    DROP JOB tg_migrator_upgrade_20240703224217
    CREATE  SCHEMA_CHANGE JOB tg_migrator_upgrade_20240703224217 {
        ADD DIRECTED EDGE freind (FROM Person, TO Person);
    }
    RUN SCHEMA_CHANGE JOB tg_migrator_upgrade_20240703224217
    """
    return ddl_upgrade

def downgrade():
    ddl_downgrade = """
    DROP JOB tg_migrator_downgrade_20240703224217
    CREATE  SCHEMA_CHANGE JOB tg_migrator_downgrade_20240703224217  {
        DROP EDGE freind;
    }
    RUN SCHEMA_CHANGE JOB tg_migrator_downgrade_20240703224217 
    """
    return ddl_downgrade
                
                
                