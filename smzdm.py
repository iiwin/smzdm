import requests
import logging  
import itchat
import time
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL





def logging_reg():
	# 第一步，创建一个logger  
	logger = logging.getLogger()  
	logger.setLevel(logging.INFO)    # Log等级总开关  
	  
	# 第二步，创建一个handler，用于写入日志文件  
	logfile = __file__.split('.')[0] + '.log'
	fh = logging.FileHandler(logfile, mode='a')  
	fh.setLevel(logging.DEBUG)   # 输出到file的log等级的开关  
	  
	# 第三步，再创建一个handler，用于输出到控制台  
	ch = logging.StreamHandler()  
	ch.setLevel(logging.DEBUG)   # 输出到console的log等级的开关  
	  
	# 第四步，定义handler的输出格式  
	formatter = logging.Formatter("%(asctime)s: %(message)s")  
	fh.setFormatter(formatter)  
	ch.setFormatter(formatter)  
	  
	# 第五步，将logger添加到handler里面  
	logger.addHandler(fh)  
	logger.addHandler(ch)  

def send_mail(sender_qq='3273863232',pwd='wsvezwwwjmbuchff',\
    receiver='651089527@qq.com',mail_title='',mail_content=''):
	#sender_qq为发件人的qq号码
	#sender_qq = '3723358***'
	#pwd为qq邮箱的授权码
	#pwd = '**iao***lxpic***'
	#收件人邮箱receiver
	#receiver='thunder***@gmail.com'
	#邮件的正文内容
	#mail_content = '你好，我是来自知乎的[邓旭东HIT] ，现在在进行一项用python登录qq邮箱发邮件的测试'
	#邮件标题
	#mail_title = '邓旭东HIT 的邮件'
    # qq邮箱smtp服务器
    host_server = 'smtp.qq.com'
    sender_qq_mail = sender_qq+'@qq.com'

    #ssl登录
    smtp = SMTP_SSL(host_server)
    #set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
    smtp.set_debuglevel(0)
    smtp.ehlo(host_server)
    smtp.login(sender_qq, pwd)

    msg = MIMEText(mail_content, "plain", 'utf-8')
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = sender_qq_mail
    msg["To"] = receiver
    smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
    smtp.quit()

    return True

def smzdm():
	BASE_URL = 'https://api.smzdm.com'
	#LOGIN_URL = BASE_URL + '/v1/user/login/normal'
	CHECKIN_URL = BASE_URL + '/v1/user/checkin'
	USER_INFO = BASE_URL + '/v1/user/info'
	CHOU_JIANG_URL= 'https://h5.smzdm.com/user/lottery/ajax_draw'

	headers = {
	    'User-Agent': 'smzdm_android_V8.3.2 rv:415 (MI MAX;Android7.0;zh)smzdmapp',
	    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		# 抽奖需要使用这个Referer
		'Referer': 'https://h5.smzdm.com/user/lottery/checkin'
	}

	cookies_ = {
		'sess': 'OTkyNjN8MTUxMjM2NDkyN3w2Nzc0NjIxNTA2fDZjYzM1NGIwY2MwN2RlZmIxYTMzYWQyN2UzMjI0YjAz',
		'device_smzdm_version': '8.3.2',
		'device_smzdm': 'android'

	}
	session = requests.Session()
	requests.utils.add_dict_to_cookiejar(session.cookies, cookies_)
	r = session.post(USER_INFO,headers=headers)

	name = r.json()['data']['display_name']
	old_jf = r.json()['data']['meta']['cpoints']
	old_jy = r.json()['data']['meta']['cexperience']
	old_jb = r.json()['data']['meta']['cgold']
	old_yz = r.json()['data']['meta']['cprestige']
	old_dj = r.json()['data']['meta']['rank']


	logging.info("=" * 30)
	logging.info("名称: " + name)
	logging.info("等级: " + old_dj)
	logging.info("积分: " + old_jf)
	logging.info("经验: " + old_jy)
	logging.info("金币: " + old_jb)
	logging.info("碎银子: " + old_yz)
	r = session.post(CHECKIN_URL,headers=headers)
	logging.info(r.json()['error_msg'])
	r = session.post(CHOU_JIANG_URL,headers=headers)
	logging.info(r.json()['error_msg'])

	r = session.post(USER_INFO,headers=headers)
	curr_jf = r.json()['data']['meta']['cexperience']
	logging.info("当前积分: " + curr_jf)
	logging.info("获得积分: " + str(int(curr_jf) - int(old_jy)))
	cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	if send_mail(mail_title=cur_time + "什么值得买: #获得积分 " + str(int(curr_jf) - int(old_jy)), mail_content='什么值得买-每日签到'):
		logging.info("已经发送邮件") 

if __name__ == '__main__':
	logging_reg()
	smzdm()
	