import struct
# from src import summary_pb2
import event_pb2
# from crc32c import crc32c
import io
import argparse


def read(data):
    header = struct.unpack('Q', data[:8])
    data = data[8:]

    # crc_hdr = struct.unpack('I', data[:4])
    data = data[4:]
    
    event_str = data[:int(header[0])]
    data = data[int(header[0]):]

    # crc_ev = struct.unpack('>I', data[:4])
    data = data[4:]
    
    return data, event_str


def save_img(encoded, step, save_gif):
    from PIL import Image
    img = Image.open(io.BytesIO(encoded))
    if save_gif:
        images.append(img)
    else:
        img.save('img_{}.png'.format(step), format='png')


parser = argparse.ArgumentParser(description='tensorboard-dumper')
parser.add_argument('--gif', default=False, action='store_true', help='save result as gif')
parser.add_argument('--input', default='demo.pb', help='saved tensorboard file to read from')
parser.add_argument('--output', default='output.gif', help='output filename for gif export')
parser.add_argument('--maxframe', default=100, help='limit the number of frames')
parser.add_argument('--duration', default=100, help='show time for each frame (ms)')

args = parser.parse_args()


try:
    with open(args.input, 'rb') as f:
        data = f.read()
except FileNotFoundError:
    print('input file not found')
    exit()

images = []

while data and args.maxframe>0:
    args.maxframe = args.maxframe-1
    data, event_str = read(data)
    event = event_pb2.Event()

    event.ParseFromString(event_str)
    if event.HasField('summary'):
        for value in event.summary.value:
            if value.HasField('image'):
                img = value.image
                save_img(img.encoded_image_string, event.step, save_gif=args.gif)
                print('img saved.')

if args.gif:
    from PIL import Image
    im = images[0]
    im.save(args.output, save_all=True, append_images=images, duration=100, loop=0) # forever
    