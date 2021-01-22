import configparser
import pymysql
from com.gusei.DefinePaths.DefinePaths import DefinePath
from imp import reload


class DbConnection:

    dbConnection = None

    @classmethod
    def getDBPropertyFile(cls):
        reload(configparser)
        config = configparser.RawConfigParser()
        config.read(DefinePath.getPropertyFilesPath() + 'config.properties')
        return dict(config.items('DB_Connections'))

    @classmethod
    def getDbConnection(cls):
        if cls.dbConnection is not None:
            return cls.dbConnection
            
        propertiesFile = DbConnection.getDBPropertyFile()

        try:
            host_name = propertiesFile.get("host_name")
            password = propertiesFile.get("password")
            port = int(propertiesFile.get("port"))
            user=propertiesFile.get("user")
            db_name=propertiesFile.get("db_name")
            connection = pymysql.connect(host = host_name,port=port, user = user,password = '',db = db_name,
                                         charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
            print('DB connection successfully established')
            return connection

        except Exception as e:
            print('DB connection failed',e)
            pass
