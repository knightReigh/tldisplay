"""
设置文件
"""

# 微博读取参数
user_id = [5491331848, 5461287018] # 杨冰怡、冯晓菲
weibo_urls = ['https://weibo.com/u/5491331848', 'https://weibo.com/u/5461287018'] # 杨冰怡、冯晓菲
filter = 0 # 取值范围为0、1，程序默认值为0，代表要爬取用户的全部微博(包括转)，1代表只爬取用户的原创微博
cookie = {"Cookie":"SSOLoginState=1524612702; ALF=1527204668; SCF=AqQguS4NUhkxgfPyNGbbZEz8-Qoo1My2h7vQ3Tj1qjRHLFwOuQ0iOjbpaeSIu1ag5XdoiVT2lH7n9ygpeTeN3xg.; SUHB=0vJY_RCN-WEkoX; _T_WM=6f33c9a8e268ce3ef50138224e2ed203; SUB=_2A253284NDeRhGeBM61sY-SzEwj6IHXVVJ9JFrDV6PUJbktBeLWT1kW1NRQbR-mXogjCOBoJf8qUQMQ88TMDL8aNC; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFvQATysoA1U3a_JyI.eB_W5JpX5K-hUgL.FoqEeh.41KzR1Kz2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMp1KM0SK-ceK.0"}
connection_timeout = 90 # request链接timeout, 秒
pause_interval = 15 # 读取微博每_页停顿一次，避免短时间内读取过多
pause_time = 5 # 读取停顿时长,秒

# 图片后缀名
image_format = ['jpg','bmp','jpeg','svg','gif','png','tiff','exif', \
                'JPG', 'BMP','JPEG','SVG','GIF','PNG','TIFF','Exif','WebP']
line_to_buffer = 20 # img_list,每_行写入文件
