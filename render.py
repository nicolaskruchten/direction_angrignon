# -*- coding: utf-8 -*-

from PIL import Image, ImageFont, ImageDraw
import unicodecsv

stations = []
with open('stations.csv', 'r') as f:
    for row in unicodecsv.DictReader(f):
        if row["end_frame"] != "0000": stations.append(row)

def get_frame(station, frame):
    return Image.open("frames/%s-%04d.png" % (station, frame))

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0, 132, 73)

sample_image = get_frame(stations[0]["code"],1)
draw = ImageDraw.Draw(sample_image)


univers = "/Users/nicolas/Library/Fonts/universcond.ttf"
arial = "/Library/Fonts/Arial Unicode.ttf"
title_font_size = 300
arrow_font = ImageFont.truetype(arial, title_font_size)
title_font = ImageFont.truetype(univers, title_font_size)
font = ImageFont.truetype(univers, 100)
copyright_font = ImageFont.truetype(univers, 50)
arrow = u"➔"
title = "ANGRIGNON"
arrow_size = draw.textsize(arrow, arrow_font)
title_size = draw.textsize(title, title_font)
box_size = ((arrow_size[0] + title_size[0])*1.15, title_size[1]*1.15)
copyright_notice = u"© NICOLAS KRUCHTEN 2016"
copyright_size = draw.textsize(copyright_notice, copyright_font)


margin = 200
left_margin = margin+draw.textsize(stations[0]["name"].upper(), font=font)[0]
top_margin = margin+500
bottom_margin = margin+100
height = sample_image.size[1]
width = height * 30
physical_width = width+height*9/16


dims = (left_margin+physical_width+margin, top_margin+height*len(stations)+bottom_margin)
box_center = (margin + physical_width/2, dims[1] - margin - box_size[1]/2)
output = Image.new('RGB', dims, BLACK)

# draw the box and right-arrow at bottom right and rotate to draw title
draw = ImageDraw.Draw(output)
draw.rectangle( (box_center[0] - box_size[0]/2, box_center[1] - box_size[1]/2, 
                 box_center[0] + box_size[0]/2, box_center[1] + box_size[1]/2,), fill=GREEN)
draw.text((box_center[0] + box_size[0]/2.2 - arrow_size[0], box_center[1] - arrow_size[1]/2 - 60), 
          arrow, WHITE, font=arrow_font)
output=output.rotate(180)
draw = ImageDraw.Draw(output)
box_center = (dims[0]-box_center[0], dims[1] - box_center[1])
draw.text((box_center[0] + box_size[0]/2.2 - title_size[0],box_center[1]  - title_size[1]/2 -30), 
          title, WHITE, font=title_font)
draw.text((box_center[0] - copyright_size[0]/2,dims[1]-bottom_margin+100), 
          copyright_notice, WHITE, font=copyright_font)
output.crop(
  (box_center[0] - copyright_size[0]/1.8, dims[1]-bottom_margin, 
   box_center[0] + copyright_size[0]/1.8, dims[1]-bottom_margin+200)
).save('output/copyright.png')

for i, s in enumerate(stations):
    station_code = s["code"]
    station_name = s["name"].upper()
    start = int(s["start_frame"])
    end = int(s["end_frame"])
    for j in range(start, end): 
        pct = float(j-start)/float(end-start)
        frame = get_frame(station_code, j)
        if station_code in ["23-DLG", "27-ANG"]: 
            frame = frame.transpose(Image.FLIP_LEFT_RIGHT)
        horiz_offset = int(width*(1-pct*pct))
        if station_code == "27-ANG":
            horiz_offset = width - horiz_offset
        output.paste(frame, (left_margin + horiz_offset, i*height+top_margin))
    name_width = draw.textsize(station_name, font)[0]
    draw.text((left_margin-name_width-50,40+i*height+top_margin), 
              station_name, WHITE, font=font)
    output.crop(
      (0,i*height+top_margin, dims[0], (i+1)*height+top_margin)
      ).save('output/%s.jpg' % station_code)

#output.show()
output.save('output/full.jpg')
output.crop(
  (box_center[0] - box_size[0]/2, box_center[1] - box_size[1]/2, 
   box_center[0] + box_size[0]/2, box_center[1] + box_size[1]/2)
).save('output/header.png')