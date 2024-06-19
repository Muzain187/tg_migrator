
import configparser
import os
from datetime import datetime
import pyTigerGraph as tg
import json
import importlib.util



class Config:
    @staticmethod
    def init(file_path):
        config = configparser.ConfigParser()
        config['tg_migrator'] = {
            'host_name': 'http://localhost:9000',
            'secret': 'your_secret',
            'tg_cloud': 'False',  # Default value; can be True or False
            'graph_name': 'your_graph',
            'token': 'your_token'
        }
        with open(file_path, 'w') as configfile:
            config.write(configfile)
        print(f"Configuration file '{file_path}' created successfully.")
   
    @staticmethod
    def read_config(file_path):
        config = configparser.ConfigParser()
        config.read(file_path)
        
        host_name = config['tg_migrator']['host_name']
        secret = config['tg_migrator']['secret']
        tg_cloud = config['tg_migrator'].getboolean('tg_cloud')
        graph_name = config['tg_migrator']['graph_name']
        token = config['tg_migrator']['token']
        
        return host_name, secret, tg_cloud, graph_name, token
    

    @staticmethod
    def create_migration(message,conn):
        # Ensure tg_migrator directory exists
        if not os.path.exists('tg_migrator'):
            os.makedirs('tg_migrator')
        
        # Create a timestamp for the migration file name
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        file_name = f"tg_migrator/{timestamp}_{message.replace(' ', '_')}.py"


        
        # Write the migration file with upgrade() and downgrade() functions
        with open(file_name, 'w') as file:
            file.write(f"""\"\"\"Migration: {message}\"\"\"
                       
\"\"\"
version id: {file_name} 
\"\"\"

def upgrade():
    ddl_upgrade = \"\"\"
    DROP JOB tg_migrator_upgrade_{timestamp}
    CREATE  SCHEMA_CHANGE JOB tg_migrator_upgrade_{timestamp} {{
        ADD VERTEX <vertex_name> (PRIMARY_ID id STRING, ....) WITH primary_id_as_attribute="true";
        ADD DIRECTED EDGE <edge_name> (FROM source, TO target);
    }}
    RUN SCHEMA_CHANGE JOB tg_migrator_upgrade_{timestamp}
    \"\"\"
    return ddl_upgrade

def downgrade():
    ddl_downgrade = \"\"\"
    DROP JOB tg_migrator_downgrade_{timestamp}
    CREATE  SCHEMA_CHANGE JOB tg_migrator_downgrade_{timestamp}  {{
        DROP VERTEX Vertex_Type_Name [',' Vertex_Type_Name]*;
        DROP EDGE Edge_Type_Name [',' Edge_Type_Name]*;
    }}
    RUN SCHEMA_CHANGE JOB tg_migrator_downgrade_{timestamp} 
    \"\"\"
    return ddl_downgrade
                
                
                """)
        print(f"Migration file '{file_name}' created successfully.")
        return file_name


class tg_config:
    @staticmethod
    def tg_connect():
        host_name, secret, tg_cloud, graph_name, token = Config.read_config('tg_migrator.ini')
        print("connecting to Tigergraph server..")
        conn = tg.TigerGraphConnection(host=host_name,graphname=graph_name, gsqlSecret=secret,tgCloud=tg_cloud)
        print("Generating auth token..")
        authToken = conn.getToken(secret)
        Token = authToken[0]
        print("Token created successfully")
        conn = tg.TigerGraphConnection(host=host_name,graphname=graph_name, gsqlSecret=secret,tgCloud=tg_cloud,apiToken=Token)
        print("Connected to Tigergraph Server..")
        return conn
    

    @staticmethod
    def tg_checkVertex(conn):
        result = conn.getVertexType("tg_migrator")
        return len(result) > 0
    
    def tg_create_migrator_vertex(conn):
        host_name, secret, tg_cloud, graph_name, token = Config.read_config('tg_migrator.ini')
       
        response = conn.gsql(
            f"USE GRAPH {graph_name}"+
            """
            DROP JOB ALL
            CREATE  SCHEMA_CHANGE JOB create_tg_migrator_vertex  {
                ADD VERTEX tg_migrator (PRIMARY_ID id STRING, active BOOL) WITH primary_id_as_attribute="true";
                ADD DIRECTED EDGE next_version (FROM tg_migrator, TO tg_migrator);
                ADD DIRECTED EDGE previous_version (FROM tg_migrator, TO tg_migrator);
            }
            RUN SCHEMA_CHANGE JOB create_tg_migrator_vertex

            INTERPRET QUERY(){
                INSERT INTO tg_migrator values("root",TRUE);
            }

            
            """
        ) 

        return response

    def tg_add_migration(conn,file_name):
        host_name, secret, tg_cloud, graph_name, token = Config.read_config('tg_migrator.ini')
        result = conn.gsql(
            f"USE GRAPH {graph_name}"+
            f"""
            INTERPRET QUERY(){{
                INSERT INTO tg_migrator values("{file_name}",FALSE);
            }}
            """
        )
        print(result)
        leaf_node =  conn.gsql(
            f"USE GRAPH {graph_name}"+
            """
            INTERPRET QUERY(){
            src = select s from tg_migrator:s WHERE s.id == "root";
            leaf = {};
            WHILE src.size() > 0
            DO
                leaf = src;
                    src = select t from src:s - (next_version>:e) - tg_migrator:t;
            END;
            PRINT leaf[leaf.id];
            }
            """
        )
        # print("Leaf Node .....")
        # print(leaf_node)
        # print(type(leaf_node))
        json_part = leaf_node.split(f"Using graph '{graph_name}'")[-1].strip()

        # Parse the JSON string into a dictionary
        data = json.loads(json_part)

        # Extract the v_id value
        v_id = data["results"][0]["leaf"][0]["v_id"]
        print(v_id)
        # print(leaf_node)
        result = conn.gsql(
            f"USE GRAPH {graph_name}"+
            f"""
            INTERPRET QUERY(){{
                INSERT INTO next_version (FROM, TO) VALUES ("{v_id}" tg_migrator, "{file_name}" tg_migrator);
                INSERT INTO previous_version (FROM, TO) VALUES ("{file_name}" tg_migrator, "{v_id}" tg_migrator);
            }}
            """
        )
        # print(result)



    def load_module_from_file(file_path):
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def tg_upgrade(conn,version):
        host_name, secret, tg_cloud, graph_name, token = Config.read_config('tg_migrator.ini')
        result = conn.gsql(
            f"USE GRAPH {graph_name}"+
            """
            INTERPRET QUERY(){
            ListAccum<STRING> @@files;
            src = SELECT s from tg_migrator:s - (next_version>:e) - tg_migrator:t WHERE s.id == "root";
            WHILE src.size()> 0 
            DO
                src = 
                SELECT t 
            from src:s - (next_version>:e) - tg_migrator:t 
             ACCUM 
  				case when t.active== FALSE THEN
  						@@files += t.id
  				END
                ;
            end;
            PRINT @@files as files;
            }

        """)
        # print(type(result))
        # print(result)
        # Extract the JSON part from the string
        json_part = result.split(f"Using graph \'{graph_name}\'")[-1].strip()

        # Parse the JSON string into a dictionary
        data = json.loads(json_part)

        # Extract the list of files
        files = data["results"][0]["files"]

        if len(files) < 1:
            print("All the version are up to date..")

        else:
            
            for filename in files:
                module = tg_config.load_module_from_file(filename)
                print(f"Executing functions in {filename}")
                
                if hasattr(module, 'upgrade'):
                    print("Executing upgrade function:")
                    upgrade_command = module.upgrade()
                    print(upgrade_command)
                    result = conn.gsql(
                        f"USE GRAPH {graph_name}"+
                        upgrade_command+
                        f"""
                        INTERPRET QUERY(){{
                            src =
                            select s from tg_migrator:s 
                            where s.id == "{filename}"
                            post-accum s.active = TRUE 
                            ;
                        }}
                        """
                    )
                    print(result)
                
                # if hasattr(module, 'downgrade'):
                #     print("Executing downgrade function:")
                #     downgrade_result = module.downgrade()
                #     print(downgrade_result)

    def tg_downgrade(conn,version):
        host_name, secret, tg_cloud, graph_name, token = Config.read_config('tg_migrator.ini')
        result = conn.gsql(
            f"USE GRAPH {graph_name}"+
            """
            INTERPRET QUERY(){
                    leaf_node = 
                    SELECT s FROM
                    tg_migrator:s 
                    where s.outdegree("next_version") == 0
                    ;
                    print leaf_node;
            }

            """)
        print(type(result))
        print(result)
        json_part = result.split(f"Using graph \'{graph_name}\'")[-1].strip()

        # Parse the JSON string into a dictionary
        data = json.loads(json_part)

        # Extract the v_id value
        v_id = data["results"][0]["leaf_node"][0]["v_id"]

        # Print the extracted v_id
        print(v_id)
        result = conn.gsql(
                f"""
                USE GRAPH {graph_name}
                INTERPRET QUERY(){{
                    ListAccum<string> @@files;
                    OrAccum @@downgradefile;
                    leafnode = select s from tg_migrator:s where s.id == "{v_id}";
                    while leafnode.size() > 0
                    do
                        leafnode = select t from leafnode:s - (previous_version>:e) - tg_migrator:t
                        ACCUM @@files += s.id,
                        if s.id == "{version}" then 
                            @@downgradefile += TRUE 
                        end
                        ;
                        if @@downgradefile then
                            break;
                        end;
                    end;
                    print @@files as files;
                         
                }}


        """)
        # Extract the JSON part from the string
        json_part = result.split('Using graph \'temporary\'')[-1].strip()

        # Parse the JSON string into a dictionary
        data = json.loads(json_part)

        # Extract the list of files
        files = data["results"][0]["files"]

        # Print the extracted files
        print(files)
        # # Extract the list of files
        # files = data["results"][0]["files"]

        if len(files) < 1:
            print("All the version are up to date..")

        else:
            
            for filename in files:
                module = tg_config.load_module_from_file(filename)
                print(f"Executing functions in {filename}")
                
                if hasattr(module, 'downgrade'):
                    print("Executing downgrade function:")
                    downgrade_command = module.downgrade()
                    print(downgrade_command)
                    result = conn.gsql(
                        f"USE GRAPH {graph_name}"+
                        downgrade_command+
                        f"""
                        INTERPRET QUERY(){{
                            src =
                            select s from tg_migrator:s 
                            where s.id == "{filename}"
                            post-accum s.active = FALSE 
                            ;
                        }}
                        """
                    )
                    print(result)