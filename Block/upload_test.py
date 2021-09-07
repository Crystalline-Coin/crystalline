from Block import Block

FILE_PATH = '/home/taha/Downloads/michael-jackson-billie-jean-128.mp3'
FILE_NAME = 'mj'
NEW_FILE_PATH = '/home/taha/Desktop'

if __name__ == '__main__':
    new_block = Block('00', '000000', 1, 1)
    new_block.upload_file(FILE_PATH)
    new_block.download_file(FILE_NAME, NEW_FILE_PATH, 0)