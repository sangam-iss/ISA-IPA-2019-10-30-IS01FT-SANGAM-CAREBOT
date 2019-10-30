import tagui as t

# #format_date = "%d/%m/%Y, %H:%M:%S"

# t.init()

# def hover_and_click(selector):
# 	t.hover(selector)
# 	str = t.click(selector)
# 	return str

doctor_name = "Padmini Ramesh"
t.init()
t.url("http://127.0.0.1:8000/")


t.click('//select[@id="txtSpecificDoc"]')
t.click('//a[@role= "option"][.="'+str(doctor_name)+'"]')


# import datetime
# import tagui as t
# from datetime import timedelta,datetime


# t.init()


# #mobile = input()



# t.url("http://127.0.0.1:8000/change_input")
# t.click('//input[@id="txtHandNo"]')
# t.type('//input[@name="txtHandNo"]', "12345678")
# t.click('//button[@id="btnsubmit"]')

# t.wait(5)


# t.click('//label[contains(.,'+str(to_date)+')]')

# def hover_and_read(selector):
# 	t.hover(selector)
# 	str = t.read(selector)
# 	return str
# num = t.count()
# n=1
# for i in range(1, num+1):
# 	booked_date[n-1]= hover_and_read(f"(//label[contains(.,'.m')])[{n}]")
# 	n+=1 
# # x=0
# # for i in booked_date:
# # 	x+=1
# # 	if i==from_date:
# # 		r=x

# t.click('//input[@name="date_id"][2]')

# t.click('//div[@class="filter-option-inner-inner"]')
# t.click('//a[@role= "option"][.='+str(apttime)+']')

# # t.click('//select[@id="txtSpecificDoc"][.="padmini"]')

# # t.click('//select[@id="ddlMin"]')
# # t.click('//select[@id="ddlMin"]/option[2]')
# # t.click('//*[@id="txtSpecificDoc"]/option[2]/html/body/div[14]/div[1]/div/div[2]/div[1]/div/div[2]/div/div/div[1]/div/div/div/div[1]/form/div[15]/div/select/option[2]')

# # t.hover('//select[@id="txtSpecificDoc"]/option[2]')

# # hover_and_click('//select[@id="txtSpecificDoc"]/option[2]')




# # t.click('//select[@id="txtSpecificDoc"]/option[contains(.,"Padmini")]')
# t.wait(5)