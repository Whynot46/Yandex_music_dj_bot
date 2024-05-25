from yandex_music import Client
import os
from dotenv import load_dotenv


load_dotenv()


def print_track_info(track):
    artists = ', '.join(artist['name'] for artist in track['artists'])
    print(f"Название: {track['title']}")
    print(f"Исполнитель: {artists}")
    print('-' * 30)


def search_tracks(client, query):
    search_results = client.search(query)
    if not search_results or not search_results.tracks:
        print("Трек не найден.")
        return []

    tracks = search_results.tracks['results']
    print("Результаты поиска:\n" + '-'*30)
    for index, track in enumerate(tracks):
        print(f'Песня под номером - {index + 1}')
        print_track_info(track)
    return tracks


def main():
    client = Client(token=os.getenv('YANDEX_MUSIC_TOKEN')).init()
    query = input('Введите название трека>>> ')
    tracks = search_tracks(client, query)
    while True:
        try:
            track_number = int(input('Введите номер подходящей песни>>> '))
            if 1 <= track_number <= len(tracks):
                selected_track = tracks[track_number - 1]
                print_track_info(selected_track)
                selected_track.download(f'./music/{selected_track["title"]}.mp3')
                print('Песня загружена')
                break
            else:
                print('Неверный номер или номер должен состоять из чисел')
        except ValueError:
            print('Неверный номер или номер должен состоять из чисел')


if __name__ == '__main__':
    main()