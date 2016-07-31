#!/bin/bash
cd videos
for f in *.MOV; do ffmpeg -i $f -vf "transpose=1,scale=-1:200" ../frames/${f%%.*}-%04d.png; done
cd ..
/opt/ImageMagick/bin/mogrify -gamma 1.6,0.6,1.0 frames/24-*
/opt/ImageMagick/bin/mogrify -gamma 1.2 frames/27-*