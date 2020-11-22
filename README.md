# BadmintonCrawler

复旦大学羽毛球场预约爬虫

每5分钟查询一次

有空场发送邮箱提醒

使用crontab执行定时任务

```bash
*/5 13-22 * * * python BadmintonCrawler.py >> log.txt 2>&1 &

```

