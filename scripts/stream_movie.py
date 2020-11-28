#!/usr/bin/python3

import argparse
import json
import os
import re
import shlex
import sys

HELP = '''
Stream a movie file to a MovieTime RTMP host.

Reads a config file in $HOME/.movie_config.json that defines the
`Host` and `Stream_Key` for the host to send the stream to and the
key for authenticating with the server.
'''

parser = argparse.ArgumentParser(prog='stream_movie', description=HELP)

parser.add_argument(
    'movie_file',
    action='store',
    type=str,
    help='Movie file to stream'
)

parser.add_argument(
    '-s',
    '--start_time',
    action='store',
    type=str,
    default='00:00:00',
    help='Optionally specify time in the movie file to start stream in the format of HH:MM:SS. Defaults to the beginning of the file.'
)

parser.add_argument(
    '-c',
    '--config_file',
    action='store',
    type=str,
    default=f"{os.getenv('HOME')}/.movie_config.json",
    help='Optionally specify config file. Defaults to $HOME/.movie_config.json'
)

args = parser.parse_args()

config_file = args.config_file

try:
    with open(config_file, 'r') as config_fp:
        config = json.load(config_fp)

        host = config['Host']
        stream_key = config['Stream_Key']
except IOError:
    print(f'ERROR: No file {config_file} found!')
    sys.exit(1)
except KeyError as exc:
    print(f'ERROR: Invalid config file! Missing key: {exc}')
    sys.exit(1)

movie_file = args.movie_file

if not os.path.exists(movie_file):
    print(f'ERROR: File {movie_file} not found!')
    sys.exit(1)

# Escape filename to ensure string is properly passed to ffmpeg
movie_file = shlex.quote(movie_file)

start_time = args.start_time

if not re.match(r'[0-9]{2}:[0-9]{2}:[0-9]', start_time):
    print(f'ERROR: Invalid start_timestamp {start_time}. Please enter a value in the form of HH:MM:SS')
    sys.exit(1)

rtmp_server = f'rtmp://{host}/live/{stream_key}'

command = f'/usr/bin/ffmpeg -ss {start_time} -re -i {movie_file} -c:v copy -b:v 301k -c:a aac -f flv {rtmp_server}'

sys.exit(os.system(command))
