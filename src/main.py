import os
import signal
import sys
import time
import requests
import zipfile
import subprocess
import psutil
import shutil
from tqdm import tqdm

class Updater:
    def __init__(self, mode, exe_path, url):
        self.mode = mode
        self.exe_path = exe_path
        self.dirPath = os.path.dirname(exe_path)
        self.url = url

    def check_url_file_type(self, url):
        try:
            response = requests.head(url)
            content_type = response.headers.get('content-type')

            if content_type == 'application/zip':
                return 'Zip file'
            elif content_type == 'application/x-msdownload':
                return 'Executable file'
            elif content_type == 'application/octet-stream':
                return 'Binary file'
            elif content_type == 'application/vnd.microsoft.portable-executable':
                return 'Portable Executable file'
            else:
                return content_type
        except requests.exceptions.RequestException:
            return None

    def download_file(self, url, local_filename):
        url_file_type = self.check_url_file_type(url)
        if url_file_type not in ['Zip file', 'Executable file', 'Binary file', 'Portable Executable file']:
            print('url không hợp lệ. Nó trỏ đến file có loại là:', url_file_type)
            input('Nhấn Enter để thoát...')
            sys.exit(0)
        print('Đang tải file cập nhật...')
        response = requests.get(url, stream=True)
        total_size_in_bytes= int(response.headers.get('content-length', 0))
        progress_bar = tqdm(total=total_size_in_bytes, unit='B', unit_scale=True)
        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                progress_bar.update(len(chunk))
                f.write(chunk)
        progress_bar.close()
        return local_filename

    def update_folder(self):
        print('Đang tải file cập nhật...')
        zip_path = "temp.zip"
        self.download_file(self.url, zip_path)
        print('Đang giải nén file cập nhật...')
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.dirPath)
        os.remove(zip_path)

    def update_file(self):
        self.download_file(self.url, self.exe_path)
    
    def removeOldFiles(self, directory):
        for filename in os.listdir(directory):
            if filename.endswith('.old'):
                os.remove(os.path.join(directory, filename))

    def rename_files_to_old(self, directory):
        self.removeOldFiles(directory)
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
        print('Kiểm tra ứng dụng đang chạy...')
        if not os.path.exists(self.exe_path):
            print(f'File hoặc thư mục {self.exe_path} không tồn tại.')
            input('Nhấn Enter để thoát...')
            sys.exit(0)
        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'] == os.path.basename(self.exe_path):
                print('Ứng dụng',process.info['name'], 'Đang chạy với pid =', process.info['pid'],'Tự động tắt ứng dụng để cập nhật.')
                try:
                    self.kill_process(process.info['pid'])
                    print('OK - Ứng dụng đã tắt.')
                except Exception as e:
                    print('Không thể tắt ứng dụng:', str(e))
                    input('Nhấn Enter để thoát...')
                    sys.exit(0)

        try:
            if self.mode.lower() == 'folder':
                self.rename_files_to_old(self.dirPath)
                self.update_folder()
                self.removeOldFiles(self.dirPath)
            elif self.mode.lower() == 'file':
                os.rename(self.exe_path, self.exe_path + '.old')
                self.update_file()
                self.removeOldFiles(self.dirPath)
            else:
                print('Chế độ không hợp lệ. Chọn "folder" hoặc "file".')
                sys.exit(0)
            print('Cập nhật thành công!')
            print('Khởi động lại ứng dụng...')
            subprocess.Popen(self.exe_path, creationflags= subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS | subprocess.CREATE_BREAKAWAY_FROM_JOB)
            print('Bye!')
            time.sleep(1)
            sys.exit(0)
        except Exception as e:
            print('Có lỗi xảy ra trong quá trình cập nhật:', str(e))
            try:
                print('Khôi phục lại các file cũ...')
                # Lấy danh sách ứng dụng đang chạy
                for filename in os.listdir(self.dirPath):
                    old_filePath = os.path.join(self.dirPath, filename + '.old')
                    new_filePath = os.path.join(self.dirPath, filename)

                    if not new_filePath.endswith('.old') and os.path.exists(old_filePath):
                        os.remove(new_filePath)
                        os.rename(old_filePath, new_filePath)
                print('Khôi phục thành công!')
            except Exception as e:
                print('Không thể khôi phục file cũ:', str(e))

if __name__ == "__main__":
    updater = Updater(sys.argv[1], sys.argv[2], sys.argv[3])
    updater.run()
