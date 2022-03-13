import smtplib
from email.mime.text import MIMEText
# email 用于构建邮件内容
from email.header import Header
# 发信方的信息：发信邮箱，QQ 邮箱授权码
from_addr = input('请输入登录邮箱：')    #'864339706@qq.com'
password = input('请输入邮箱授权码：')   #'oubyucmcuaepbfai'
# 收信方邮箱
to_addr =input('请输入收信方邮箱')       #'864339706@qq.com'

# 发信服务器
smtp_server = 'smtp.qq.com'

# 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
text=input('请输入要发送的文本')
#'''这是2.0版本啦!\n可以写好长的话\n我就试试到底可以写多长\n猪看哈利波特就好啦\n我搞定3.0版本就先不学了hhh\n'''                                    #邮件内容
msg = MIMEText(text ,'plain','utf-8')
writer=input('请输入写信人名称')        #发邮件人名称
receiver=input('请输入收信人名称')      #收件人名称
email_name=input('请输入邮件名称')       #邮件名称 
msg['From'] = Header(writer)         
msg['To'] = Header(receiver)         
msg['Subject'] = Header(email_name)     #邮件名称
# smtplib 用于邮件的发信动作
# 开启发信服务，这里使用的是加密传输
server = smtplib.SMTP_SSL()
server.connect(smtp_server,465)
# 登录发信邮箱
server.login(from_addr, password)
# 发送邮件
server.sendmail(from_addr, to_addr, msg.as_string())
# 关闭服务器
server.quit()