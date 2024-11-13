import crawlers.downloader as dl
from config.secrets import vbs_start_date, vbs_end_date

if __name__ == '__main__':
    dl.login()
    dl.download_ati(vbs_start_date, vbs_end_date)
    dl.download_mictsi(vbs_start_date, vbs_end_date)