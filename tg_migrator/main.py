# main.py

from config import Config, tg_config
import sys

def main():
    print("""
 ________ _____   __  __ ______ ____ _____         ________ ___  _____  
 |__   __/ ____| |  \/  |_   _/ ____|  __ \     /\|__   __/ __ \|  __ \ 
    | | | |  __  | \  / | | || |  __| |__) |   /  \  | | | |  | | |__) |
    | | | | |_ | | |\/| | | || | |_ |  _  /   / /\ \ | | | |  | |  _  / 
    | | | |__| | | |  | |_| || |__| | | \ \  / ____ \| | | |__| | | \ \ 
    |_|  \_____| |_|  |_|_____\_____|_|  \_\/_/    \_\_|  \____/|_|  \_\
             ______                                                     
            |______|  
                                                            
    By: Mohammad Ashraf
    Version: 0.1.2

    """)
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'init':
            config_file_path = 'tg_migrator.ini'
            Config.init(config_file_path)

        elif command == 'create_version' and len(sys.argv) > 3 and sys.argv[2] == '-m':
            message = sys.argv[3]
            conn = tg_config.tg_connect()
            if not tg_config.tg_checkVertex(conn):
                print("creating tg_migrator ...")
                print(tg_config.tg_create_migrator_vertex(conn))

            file_name = Config.create_migration(message)
            tg_config.tg_add_migration(conn, file_name)

        elif command == 'upgrade' and len(sys.argv) > 2:
            version = sys.argv[2]
            if version == "all":
                conn = tg_config.tg_connect()
                tg_config.tg_upgrade(conn, version)

        elif command == "downgrade" and len(sys.argv) > 2:
            version = sys.argv[2]
            conn = tg_config.tg_connect()
            tg_config.tg_downgrade(conn, version)
        
    else:
        print("""
        Options                             Descriptions 
        ---------------------------------------------------------------------------------------------
        init                                initialize the project
        create_version -m                   creating the version followed by the message
        upgrade all                         upgrading the versions one by one
        downgrade <version_id>              downgrading the version from last to specified <version_id>      

        """)

if __name__ == "__main__":
    main()
