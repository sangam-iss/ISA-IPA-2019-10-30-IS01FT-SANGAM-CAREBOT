# tagui_lib.py	
# 190708
# CK

import tagui as t

def wait_for_pageload(selector):
	wait_status = 0
	for loop_wait in range(1, 60):
		print(f"{loop_wait}. waiting for page to appear. wait for 1s...")
		if t.present(selector):
			wait_status = 1
			break
		else:
			t.wait(1)
	print("bp801.2 wait_status = {}".format(wait_status))

def hover_and_read(selector):
	t.hover(selector)
	str = t.read(selector)
	return str
