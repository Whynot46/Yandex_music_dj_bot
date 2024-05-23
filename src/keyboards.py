from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
import src.yandex_music_api as yandex


main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Найти трек🔎')]],
    resize_keyboard=True)


download_keyboard = track_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Скачено", callback_data=f"was_download")]
    ])


add_keyboard = track_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Добавлено", callback_data=f"was_add")]
    ])


playlist_keyboard = track_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Скачать плейлист", callback_data=f"playlist")]
    ])


def generate_track_keyboard(track_name):
    track_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Скачать", callback_data=f"download-{track_name}"),
        InlineKeyboardButton(text="Добавить в плейлист", callback_data=f"add-{track_name}")
        ]
    ])
    return track_keyboard


def generate_tracks_keyboard(track_name):
    buttons = []
    tracks = yandex.get_tracks(track_name)
    for track in tracks[:5]:
        title, artists = yandex.get_info(track)        
        buttons.append([InlineKeyboardButton(text=f"{str(artists)}-{str(title)}"
                                            , callback_data=f"{artists}-{title}"
                                            )
                        ])
    tracks_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return tracks_keyboard