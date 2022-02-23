from dotenv import load_dotenv
import os
import glob
import shutil

load_dotenv()

def main():
	torrent_path = os.environ['torrent_path']

	base_show_name = os.path.basename(torrent_path)
	torrent_top_dir = os.path.dirname(torrent_path)

	if base_show_name.partition(' ')[0] == 'Season':
		base_show_name = os.path.basename(os.path.dirname(torrent_path))

	# Store all files in torrent directory to
	media_files = sorted(glob.glob(f'{torrent_path}/*'))

	# Form the top level dir for the show in plex directory
	anime_dir_in_plex = f"{os.environ['plex_tv']}/{base_show_name}"

	prepare_files_for_plex(media_files, torrent_path)
	# Top level dir of show may exist given an additional season is added later
	# dirs_exist_ok must be True
	shutil.copytree(torrent_top_dir, anime_dir_in_plex, dirs_exist_ok=True)

	# Needs to be visible by plex in order to load
	os.system(f'chmod 777 -R {anime_dir_in_plex}')

	shutil.rmtree(torrent_path)

def prepare_files_for_plex(media_files: list, torrent_path: str) -> None:
	# Ugly, but need to get the number of digits in the max epsiode number in order to pad
	# 0s to the episode count accordingly
	# Constant of 1 added to exclude existing digit
	pad_factor = len(str(len(media_files))) + 1

	for idx in range(0, len(media_files)):
		ep_num = f' - s02e{str(idx+1).zfill(pad_factor-len(str(idx+1)))} - '

		media_name = os.path.basename(media_files[idx])
		dot_sep = media_name.rindex('.')

		new_media_name =  'Shokugeki_no_Souma' + ep_num + media_name[dot_sep:]
		os.rename(media_files[idx], f'{torrent_path}/{new_media_name}')

if __name__ == '__main__':
	main()