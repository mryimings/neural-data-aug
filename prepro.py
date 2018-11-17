import argparse
import os
import re
from shutil import copyfile

def prepro(src_dir, dst_dir, info_file):
    pic_style_map = {}
    filename_pattern = r"[0-9]+\.jpg"
    with open(info_file, "r") as f:
        next(f)
        for line in f:
            items = line.split(',')
            filename = items[0]
            assert re.match(filename_pattern, filename)
            style = items[-3].replace(" ", "-").replace("(", "").replace(")", "")
            pic_style_map[filename] = style

    for pic in os.listdir(src_dir):
        if not re.match(filename_pattern, pic):
            continue
        if not pic in pic_style_map:
            print(pic, "is not in the", info_file)
            continue
        style = pic_style_map[pic]
        if style == '':
            style = "style-missing"
        style_dir = os.path.join(dst_dir, style)
        if not os.path.exists(style_dir):
            os.makedirs(style_dir)
        copyfile(os.path.join(src_dir, pic), os.path.join(style_dir, pic))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--src_dir")
    parser.add_argument("--dst_dir")
    parser.add_argument("--info_file")
    args = parser.parse_args()
    prepro(src_dir=args.src_dir, dst_dir=args.dst_dir, info_file=args.info_file)