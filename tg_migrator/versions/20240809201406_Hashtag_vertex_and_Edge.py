"""Migration: Hashtag vertex and Edge"""
                       
"""
version id: versions/20240809201406_Hashtag_vertex_and_Edge.py 
"""

def upgrade():
    ddl_upgrade = """
    DROP JOB tg_migrator_upgrade_20240809201406
    CREATE  SCHEMA_CHANGE JOB tg_migrator_upgrade_20240809201406 {
        ADD VERTEX Hashtag (PRIMARY_ID id STRING) WITH primary_id_as_attribute="true";
        ADD DIRECTED EDGE has_tag (FROM Post, TO Hashtag);
    }
    RUN SCHEMA_CHANGE JOB tg_migrator_upgrade_20240809201406
    """
    return ddl_upgrade

def downgrade():
    ddl_downgrade = """
    DROP JOB tg_migrator_downgrade_20240809201406
    CREATE  SCHEMA_CHANGE JOB tg_migrator_downgrade_20240809201406  {
        DROP VERTEX Hashtag;
        DROP EDGE has_tag;
    }
    RUN SCHEMA_CHANGE JOB tg_migrator_downgrade_20240809201406 
    """
    return ddl_downgrade
                
                
                