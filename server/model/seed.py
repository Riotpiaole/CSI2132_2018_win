from sqlalchemy import create_engine
import psycopg2 

def connect ( host = '127.0.0.1' , port= 5432 , dbname="Term_project",
      user ='postgres'  , passwd = "locartrock" ):
    return psycopg2.connect ( "dbname = '{}' user= '{}' host = '{}' port = {} password = '{}' "\
            .format(dbname ,user ,host , port , passwd ) )

db = create_engine( '')