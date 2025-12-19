from crontab import CronTab

cron = CronTab(user=True)
BASE_DIR = "/mnt/e/labs/Microsoft Elevate Training Center/Belajar Fundamental Pemrosesan Data/ETL Pipelines/scraping-exercise"

job = cron.new(
    command=f'"{BASE_DIR}/.venv/bin/python" "{BASE_DIR}/intermediate_scraping.py" >> "{BASE_DIR}/scraping.log" 2>&1',
    comment="Scraping bookstoscrape"
)

job.minute.every(3)

cron.write()
print("Data scraping has been scheduled.")
