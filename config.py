"""
设置文件
"""

# 微博读取参数
user_id = [5491331848, 5461287018] # 杨冰怡、冯晓菲
filter = 0 # 取值范围为0、1，程序默认值为0，代表要爬取用户的全部微博(包括转)，1代表只爬取用户的原创微博
cookie = {"Cookie":"_T_WM=efd21a0dba0f5a1504c293a195801e63; SUB=_2A253dgV-DeRhGeNH7FEQ9S7KzzuIHXVUmKs2rDV6PUJbkdBeLUHxkW1NSpoOVxM-fws1iAOfmxGpPMYt7AgZJ7nf; SUHB=0FQrfXsPRm2zcb; SCF=Ap3UoqD_tiJ_KAeMT7bH_kON90wGhkBm1BXjO15wpfg-MvOV2-JbHI-MC7ixnntKv5T11l-wnVweej4GVsPYNDs.; SSOLoginState=1517450542"}
connection_timeout = 90 # request链接timeout, 秒
pause_interval = 15 # 读取微博每_页停顿一次，避免短时间内读取过多
pause_time = 5 # 读取停顿时长,秒

# 图片后缀名
image_format = ['jpg','bmp','jpeg','svg','gif','png','tiff','exif', \
               'JPG', 'BMP','JPEG','SVG','GIF','PNG','TIFF','Exif','WebP']

line_to_buffer = 20 # img_list,每_行写入文件

new_cookie = {"Cookie":""}
