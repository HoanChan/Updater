# Updater

Đây là một ứng dụng `console` hỗ trợ việc cập nhật ứng dụng. Nó hỗ trợ 2 chế độ làm việc

- Cập nhật thư mục ứng dụng từ link của một file `.Zip`
- Cập nhật file ứng dụng từ link file đó, ví dụ như file `.Exe` chẳn hạn

### Cách sử dụng:

Gọi và truyền tham số cho `Updater` như sau:

```text
Updater.exe mode exePath link
```


**Ví dụ 1:** Cập nhật thư mục ứng dụng từ link của một fie `.Zip`

```text
Updater.exe Folder D:\app\my_app.exe https://github.com/User/app/raw/main/app_v2.0.zip
```

**Ví dụ 2:** Cập nhật file ứng dụng từ link file đó, ví dụ như file `.Exe` chẳn hạn

```text
Updater.exe File D:\app\my_app.exe https://github.com/User/app/raw/main/app_v2.0.exe
```

### Cách hoạt động:

**B1:** Kiểm tra xem ứng dụng cần cập nhật cho đang chạy không, nếu có thì sẽ thông báo và yêu cầu tắt ứng dụng đó.
**B2:** Kiểm tra chế làm việc, nếu là `Folder` thì sẽ tải file `.Zip` về và giải nén vào thư mục ứng dụng, nếu là `File` thì sẽ tải file ứng dụng về và thay thế file cũ.
**B3:** Sau khi cập nhật xong, sẽ thông báo và mở ứng dụng lên.

### Lưu ý:

- Ứng dụng cần cập nhật không được chạy khi cập nhật.
- File `.Zip` hoặc file ứng dụng cần cập nhật phải là file trực tiếp, không được chứa trong thư mục khác.

### Nhắn nhủ:

Nếu bạn thấy ứng dụng này hữu ích, hãy để lại một `Star` cho tôi nhé. Cảm ơn bạn đã sử dụng ứng dụng của tôi.

<hr>


# Updater

This is a `console` application that supports updating applications. It supports 2 working modes

- Update the application directory from the link of a `.Zip` file
- Update the application file from that file link, such as the `.Exe` file

### How to use:

Call and pass parameters to `Updater` as follows:

```text
Updater.exe mode exePath link
```

**Example 1:** Update the application directory from the link of a `.Zip` file

```text
Updater.exe Folder D:\app\my_app.exe https://github.com/User/app/raw/main/app_v2.0.zip
```

**Example 2:** Update the application file from that file link, such as the `.Exe` file

```text
Updater.exe File D:\app\my_app.exe https://github.com/User/app/raw/main/app_v2.0.exe
```

### How it works:

**Step 1:** Check if the application to be updated is running, if so, it will notify and require you to close that application.
**Step 2:** Check the working mode, if it is `Folder` then it will download the `.Zip` file and extract it into the application directory, if it is `File` then it will download the application file and replace the old file.
**Step 3:** After updating, it will notify and open the application.

### Note:

- The application to be updated should not be running during the update.
- The `.Zip` file or the application file to be updated must be a direct file, not contained in another folder.

### Reminder:

If you find this application useful, please leave a `Star` for me. Thank you for using my application.
