
from config import Config,tg_config
import sys



def main():
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == 'init':
             # Path to your INI file
            config_file_path = 'tg_migrator.ini'
            Config.init(config_file_path)

        elif command == 'create_version' and len(sys.argv) > 3 and sys.argv[2] == '-m':
            message = sys.argv[3]
            conn = tg_config.tg_connect()
            print(tg_config.tg_checkVertex(conn))
            if  tg_config.tg_checkVertex(conn) is False:
                print("vertex is creating...")
                print(tg_config.tg_create_migrator_vertex(conn))
            
            file_name = Config.create_migration(message,conn)
            tg_config.tg_add_migration(conn,file_name)

        elif command == 'upgrade' and len(sys.argv) > 2:
            version = sys.argv[2]
            conn = tg_config.tg_connect()
            tg_config.tg_upgrade(conn,version)
        
        elif command == "downgrade" and len(sys.argv) > 2:
            version = sys.argv[2]
            conn = tg_config.tg_connect()
            tg_config.tg_downgrade(conn,version)



if __name__ == "__main__":
    main()
