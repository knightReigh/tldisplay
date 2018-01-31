"""
设置文件
"""

# 微博读取参数
user_id = [5491331848, 5461287018] # 杨冰怡、冯晓菲
filter = 0 # 取值范围为0、1，程序默认值为0，代表要爬取用户的全部微博(包括转)，1代表只爬取用户的原创微博
cookie = {"Cookie":"_T_WM=99ce2a087b44cc10bb3fa7d7cb59aeff; SCF=Ama1IQYsfc4Un6sJdVxQ2yxO7QQewhCh0CosukbQpTKeyao1wHIGExPmWE5gno30u_O_aNllUMa8mQq3l_TgLZE.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWvW0Jk66DBo_dquLugAH8g5JpX5K-hUgL.Fo-4S0epSK5cShM2dJLoIEvJi--fiK.7iKn0i--NiKnpi-8Fi--4iK.XiKnfi--NiKLWiKnXi--NiKyhi-8FP7tt; SUB=_2A253dKdPDeRhGeNH7FEQ9S7KzzuIHXVUlskHrDV6PUJbkdBeLVrXkW1NSpoOVzZtrQbp_o2Uszczj8ZoGWtiUq1s; SUHB=0S7C-iogZ08Z9k; SSOLoginState=1517344543"}
connection_timeout = 90 # request链接timeout, 秒
pause_interval = 15 # 读取微博每_页停顿一次，避免短时间内读取过多
pause_time = 5 # 读取停顿时长,秒

# 图片后缀名
image_format = ['jpg','bmp','jpeg','svg','gif','png','tiff','exif', \
               'JPG', 'BMP','JPEG','SVG','GIF','PNG','TIFF','Exif','WebP']

line_to_buffer = 20 # img_list,每_行写入文件
