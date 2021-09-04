import YouTube
from spotify import create_playlist, get_playlist_id, add_song_to_playlist


def main():
    all_song_info = YouTube.youtube_initiate()
    playlist = create_playlist(name= "Playlist Name HERE", public =False)
    playlist_id = get_playlist_id(playlist)
    add_song_to_playlist(playlist_id,all_song_info)


if __name__ == '__main__':
    main()   