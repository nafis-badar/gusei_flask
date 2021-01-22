import configparser
from imp import reload
from com.gusei.DefinePaths.DefinePaths import DefinePath

class ReadConstants:

    def get_constant_object(self, file_name, required_list):
        reload(configparser)
        config = configparser.RawConfigParser()
        # config.read(DefinePath.getMessagesFilePath() + 'response_messages_list.properties')
        config.read(DefinePath.getMessagesFilePath() + file_name)
        return dict(config.items(required_list))

