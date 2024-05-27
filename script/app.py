import get_download_link
import get_lawa_file
import upload_file_s3
import os


if __name__ == "__main__":
    download_link = get_download_link.lawa_download_link_groundwater()
    path = get_lawa_file.download_excel_workbook(download_link)
    upload_file_s3.upload_file_s3(path, None)
