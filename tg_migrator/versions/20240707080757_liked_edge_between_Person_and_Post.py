"""Migration: liked edge between Person and Post"""
                       
"""
version id: versions/20240707080757_liked_edge_between_Person_and_Post.py 
"""

def upgrade():
    ddl_upgrade = """
    DROP JOB tg_migrator_upgrade_20240707080757
    CREATE  SCHEMA_CHANGE JOB tg_migrator_upgrade_20240707080757 {
        ADD DIRECTED EDGE liked (FROM Person, TO Post);
    }
    RUN SCHEMA_CHANGE JOB tg_migrator_upgrade_20240707080757
    """
    return ddl_upgrade

def downgrade():
    ddl_downgrade = """
    DROP JOB tg_migrator_downgrade_20240707080757
    CREATE  SCHEMA_CHANGE JOB tg_migrator_downgrade_20240707080757  {
        DROP EDGE liked;
    }
    RUN SCHEMA_CHANGE JOB tg_migrator_downgrade_20240707080757 
    """
    return ddl_downgrade
                
                
                