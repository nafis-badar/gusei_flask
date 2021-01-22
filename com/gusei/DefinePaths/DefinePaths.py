import os


class DefinePath:
    script_path = os.path.abspath(__file__)
    folder_path = os.path.split(script_path)
    project_folder = folder_path[0]

    @classmethod
    def getPropertyFilesPath(cls):
        return str(os.path.join(cls.project_folder, '..', 'controller', 'properties_file/'))

    @classmethod
    def getLogFilePath(cls):
        return str(os.path.join(cls.project_folder, '..', 'controller', 'log_file/'))


    @classmethod
    def getMessagesFilePath(cls):
        return str(os.path.join(cls.project_folder, '..', 'controller', 'constants/'))


    @classmethod
    def get_karaoke_folder_path(cls):
        return str(os.path.join(cls.project_folder, '..', 'controller', 'media','karaoke/'))