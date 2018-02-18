import struct
# from src import summary_pb2
import event_pb2
# from crc32c import crc32c
import io
with open('demo.pb', 'rb') as f:
    data = f.read()

def read(data):
    header = struct.unpack('Q', data[:8])
    # print('header:', header)
    # print('expected header crc:',masked_crc32c(header))
    # print(header)
    data = data[8:]
    # print(data[:4])

    crc_hdr = struct.unpack('I', data[:4])
    # print('read header crc:',crc_hdr)
    # print([hex(i) for i in crc_hdr])
    data = data[4:]
    
    event_str = data[:int(header[0])]
    # print([hex(i) for i in event_str])
    data = data[int(header[0]):]

    crc_ev = struct.unpack('>I', data[:4])
    # print([hex(i) for i in crc_ev])
    data = data[4:]
    
    return data, event_str
    # print(len(event_str))
    summ = event_pb2.Event()
    # summ = summary_pb2.Summary()
    summ.ParseFromString(event_str)
    print(summ)
    return data


def save_img(encoded, step):
    from PIL import Image
    img = Image.open(io.BytesIO(encoded))
    img.save('img_{}.png'.format(step), format='png')


while data:
    data, event_str = read(data)
    event = event_pb2.Event()

    # summ = summary_pb2.Summary()
    event.ParseFromString(event_str)
    if event.HasField('summary'):
        for value in event.summary.value:
            if value.HasField('image'):
                img = value.image
                save_img(img.encoded_image_string, event.step)
                print('img')

    # print(event)
