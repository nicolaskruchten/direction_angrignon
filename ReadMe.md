## Direction Angrignon

Steps to build the output:

1. Record videos, save them in a `videos` directory and name them according to the `stations.csv` spreadsheet
2. Run the `extract_frames.sh` script which dumps all the video frames to PNG and colour-corrects a couple of stations
3. Go through each station and find the first frame number that shows movement, and the last frame number that shows the platform, and record those in `stations.csv`
4. run `render.py` to build the final output
