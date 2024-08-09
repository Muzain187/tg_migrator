"""Migration: liked vertex"""
                       
"""
version id: versions/20240707080142_liked_vertex.py 
"""

def upgrade():
    ddl_upgrade = """
    DROP JOB tg_migrator_upgrade_20240707080142
    CREATE  SCHEMA_CHANGE JOB tg_migrator_upgrade_20240707080142 {
        ADD VERTEX Post (PRIMARY_ID id STRING,content STRING) WITH primary_id_as_attribute="true";
    }
    RUN SCHEMA_CHANGE JOB tg_migrator_upgrade_20240707080142
    """
    return ddl_upgrade

def downgrade():
    ddl_downgrade = """
    DROP JOB tg_migrator_downgrade_20240707080142
    CREATE  SCHEMA_CHANGE JOB tg_migrator_downgrade_20240707080142  {
        DROP VERTEX Post;
        
    }
    RUN SCHEMA_CHANGE JOB tg_migrator_downgrade_20240707080142 
    """
    return ddl_downgrade
                
                
                