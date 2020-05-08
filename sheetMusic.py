from PIL import Image, ImageDraw, ImageFont
from math import floor
import sys

def draw_title(title, font, img, width, height):
    w,h = font.getsize(title)
    draw = ImageDraw.Draw(img)
    draw.text(((width-w)/2, (height-h)/12), title, font=font, fill="black")

def draw_staff(img, width, height, i):
    draw = ImageDraw.Draw(sheet_music)
    draw.line([(width/12,height/8 + i*160), (11*width/12, 3508/8 + i*160)], fill="black", width=3)
    draw.line([(width/12,height/8+20 + i*160), (11*width/12, height/8+20 + i*160)], fill="black", width=3)
    draw.line([(width/12,height/8+40 + i*160), (11*width/12, height/8+40 + i*160)], fill="black", width=3)
    draw.line([(width/12,height/8+60 + i*160), (11*width/12, height/8+60 + i*160)], fill="black", width=3)
    draw.line([(width/12,height/8+80 + i*160), (11*width/12, height/8+80 + i*160)], fill="black", width=3)
    draw.line([(width/12,height/8+80 + i*160), (width/12, height/8 + i*160)], fill="black", width=3)
    draw.line([(11*width/12,height/8+80 + i*160), (11*width/12, height/8 + i*160)], fill="black", width=3)

    length = 11*width/12 - width/12
    for x in range(1, 5):
        draw.line([(width/12 + x*length/5,height/8+80 + i*160), (width/12 + x*length/5, height/8 + i*160)], fill="black", width=3)

def draw_notes(img, width, height, drums, ts, f, bps):
    #Quarter note dimensions: 25x20
    #between 438.5 and 458.5
    num_notes = len(drums)
    draw = ImageDraw.Draw(img)

    for i in range(num_notes):
        cur_drum = drums[i]
        cur_ts = int(ts[i])
        cur_row = floor(cur_ts/21)

        if cur_drum == 'b':
            cur_y_index = 60
        elif cur_drum == 's':
            cur_y_index = 20
        else:
            cur_y_index = 0

        length = 11*width/12 - width/12
        indent = (length/5)/8
        measure_num = floor(i/4) % 5
        note_idx = i%4

        if f[i] == "1":
            draw.ellipse([(width/12 + indent + (length/5)*measure_num + note_idx*2*indent,height/8 + cur_y_index + cur_row * 160), (width/12 + note_idx*2*indent + indent + 25 + (length/5)*measure_num,height/8 + cur_y_index + cur_row * 160 + 20)], fill="black", width=3)
            draw.line([(width/12 + indent + (length/5)*measure_num + note_idx*2*indent + 20,height/8 + cur_y_index + cur_row * 160 + 20), (width/12 + note_idx*2*indent + indent + 25 + (length/5)*measure_num,height/8 + cur_y_index + cur_row * 160 + 20-70)], fill="black", width=5)

        else:
            draw.line([(width/12 + indent + (length/5)*measure_num + note_idx*2*indent -10,height/8 + cur_y_index + cur_row * 160 + 20), (width/12 + note_idx*2*indent + indent + 25 + (length/5)*measure_num -10,height/8 + cur_y_index + cur_row * 160 + 20-20)], fill="black", width=3)
            draw.line([(width/12 + indent + (length/5)*measure_num + note_idx*2*indent + 10,height/8 + cur_y_index + cur_row * 160 + 20), (width/12 + note_idx*2*indent + indent + 25 + (length/5)*measure_num - 30,height/8 + cur_y_index + cur_row * 160 + 20-20)], fill="black", width=3)
            draw.line([(width/12 + indent + (length/5)*measure_num + note_idx*2*indent + 10,height/8 + cur_y_index + cur_row * 160 + 20), (width/12 + note_idx*2*indent + indent + 25 + (length/5)*measure_num - 5,height/8 + cur_y_index + cur_row * 160 + 20-70)], fill="black", width=5)


def parse_notes(filename):
    drum = []
    timestamp = []
    force = []
    with open(filename) as file:
        for row in file:
            items = row.strip().split(',')
            drum.append(items[0])
            timestamp.append(round(float(items[1])))
            force.append(items[2])

    return drum, timestamp, force

if __name__ == '__main__':
    arg_len = len(sys.argv)
    if arg_len < 3:
        sys.exit()

    drums, timestamps, force = parse_notes(sys.argv[1])
    bpm = int(sys.argv[2])
    bps = bpm/60

    sheet_music = Image.new('RGBA', (2480, 3508), 'white')

    title = "Sample Sheet Music"
    font = ImageFont.truetype("arimo/Arimo-Regular.ttf", 75)
    draw_title(title, font, sheet_music, 2480, 3508)

    for i in range(0, 15):
        draw_staff(sheet_music, 2480, 3508, i)

    draw_notes(sheet_music, 2480, 3508, drums, timestamps, force, bps)

    sheet_music.save("music.png")
    #sheet_music.show()
