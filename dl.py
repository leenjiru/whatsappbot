from pytube import YouTube
from moviepy.editor import *
import os
from json import dumps, loads

from youtube_search import YoutubeSearch
#
# results = YoutubeSearch('alan walker - faded', max_results=3).to_json()


class MySearch(YoutubeSearch):
    """
    class which makes a youtube search for a song, saves the search results to a file and gives a printable result
    :param sid: chat_id of user who is downloading the song
    :param search_terms: the keywords of the song being searched
    """
    def __init__(self, search_terms: str, sid):
        super().__init__(search_terms, max_results=5)
        self.sid = sid
        self.user_directory = f'music/{self.sid}'
        self.URLS_FILE = os.path.join(self.user_directory, 'YOUTUBE_LINKS.txt')

    def user_directory_exists(self):
        return os.path.exists(self.user_directory)

    def create_user_directory(self):
        os.mkdir(self.user_directory)

    def save_to_file(self, json_result):
        """
        This function saves the search results to a file. contents are a dictionary in string
        """
        if not self.user_directory_exists():
            self.create_user_directory()
        file = open(self.URLS_FILE, 'w')
        file.write(json_result)

    def get_printable(self):
        """
        this function saves search results to file, and also gives printable result to send to whatsapp
        :return: a string containing the song titles from the search
        """
        dict_result = self.to_dict()
        result = ''
        for index, item in enumerate(dict_result):
            result += f'{index + 1}. - {item["title"]}\n'
        self.save_to_file(dumps(dict_result))
        return result


class YtSearch:
    def __init__(self, choice: dict):
        self.choice = choice
        self.vid = self.choice['id']
        self.thumbnails = self.choice['thumbnails']
        self.title = self.choice['title']
        self.url = self.choice['url_suffix']

    def __str__(self):
        return self.title

    def get_url(self):
        return f"https://youtube.com{self.url}"


class DlSelector:
    def __init__(self, sid, choice: int):
        self.sid = sid
        self.choice = choice
        self.user_directory = f'music/{self.sid}'
        self.URLS_FILE = os.path.join(self.user_directory, 'YOUTUBE_LINKS.txt')

    def read_urls(self):
        file = open(self.URLS_FILE)
        contents = file.read()
        return contents

    def get_choice_url(self):
        contents = loads(self.read_urls())
        selected = YtSearch(contents[self.choice-1])
        return selected.get_url()


class Downloader(DlSelector):
    def __init__(self, sid, choice: int):
        super().__init__(sid, choice)
        self.url = self.get_choice_url()

    def download_audio(self):
        yt = YouTube(self.url)
        print(f'[*] downloading song...')
        downloaded_path = yt.streams.filter(only_audio=True).first().download(self.user_directory)
        return downloaded_path


# downloader = Downloader(12345, 1)
# print(f'downloaded file path: {downloader.download_audio()}')

# yt = YouTube('https://www.youtube.com/watch?v=974iac8LwZY')

# print(yt.streams.filter(only_audio=True).first().download('music/steve'))


class Converter:
    def __init__(self, video_path):
        self.file_path = video_path
        self.audio_path = self.get_audio_path()

    def get_audio_path(self):
        return " ".join(self.file_path.split('.')[:-1]) + '.mp3'

    def convert(self):
        a_c = AudioFileClip(self.file_path)
        a_c.write_audiofile(self.audio_path)
        return os.path.basename(self.audio_path)


# path = "C:\\Users\\steven\\PycharmProjects\\fwhatsapp\\music/12345\\Martin Garrix & Dua Lipa - Scared To Be Lonely (Official Video).mp4"
# dl = Converter(path)
# print(dl.convert())
# converting video to audio
# file = 'alan.mp4'
# audio = 'alan.mp3'

# video_clip = VideoFileClip(file)
# audio_clip = video_clip.audio

# print('[*] converting...')
# audio_clip.write_audiofile(audio)