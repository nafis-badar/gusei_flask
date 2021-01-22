from mutagen.mp3 import MP3
# function to convert the seconds into readable format
class Music:

    def get_file_duration(self,filename):
        audio = MP3(filename)
        audio_info = audio.info
        length_in_secs = int(audio_info.length)
        return length_in_secs