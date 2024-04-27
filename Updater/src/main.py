import os
import sys
import requests
import zipfile
import subprocess
import psutil
from tqdm import tqdm

class Updater:
    def __init__(self, mode, exe_path, url):
        self.mode = mode
        self.exe_path = exe_path
        self.url = url

    def download_file(self, url, local_filename):
        response = requests.get(url, stream=True)
        total_size_in_bytes= int(response.headers.get('content-length', 0))
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                progress_bar.update(len(chunk))
                f.write(chunk)
        progress_bar.close()
        return local_filename

    def update_folder(self):
        zip_path = "temp.zip"
        self.download_file(self.url, zip_path)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(self.exe_path))
        os.remove(zip_path)

    def update_file(self):
        self.download_file(self.url, self.exe_path)

    def rename_files_to_old(self, directory):
        for filename in os.listdir(directory):
            os.rename(os.path.join(directory, filename), os.path.join(directory, filename + '.old'))

    def restore_old_files(self, directory):
        for filename in os.listdir(directory):
            if filename.endswith('.old'):
                os.rename(os.path.join(directory, filename), os.path.join(directory, filename[:-4]))

    def kill_process(self, pid):
        process = psutil.Process(pid)
        process.terminate()

    def run(self):
        if not os.path.exists(self.exe_path):
            print(f'File hoặc thư mục {self.exe_path} không tồn tại.')
            input('Nhấn Enter để thoát...')
            sys.exit(1)

        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'] == os.path.basename(self.exe_path):
                print('Tự động tắt ứng dụng...')
                self.kill_process(process.info['pid'])

        try:
            if self.mode.lower() == 'folder':
                self.rename_files_to_old(os.path.dirname(self.exe_path))
                self.update_folder()
            elif self.mode.lower() == 'file':
                os.rename(self.exe_path, self.exe_path + '.old')
                self.update_file()
            else:
                print('Chế độ không hợp lệ. Chọn "folder" hoặc "file".')
                sys.exit(1)

            subprocess.Popen(self.exe_path)
            print('Cập nhật thành công!')
        except Exception as e:
            print('Có lỗi xảy ra trong quá trình cập nhật:', str(e))
            print('Khôi phục lại các file cũ...')
            if self.mode.lower() == 'folder':
                self.restore_old_files(os.path.dirname(self.exe_path))
            elif self.mode.lower() == 'file':
                os.rename(self.exe_path + '.old', self.exe_path)
            print('Khôi phục thành công!')

if __name__ == "__main__":
    updater = Updater(sys.argv[1], sys.argv[2], sys.argv[3])
    updater.run()
