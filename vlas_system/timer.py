import time
def control_timer(queue, duration = {'unit':"seconds", "amount":0}, start = True, status_check = False):
	##
	# Function that starts, stops and checks status of timer
	# @param queue: queue used to update GUI thread
	# @param dictionary containing time unit and duration to start timer
	# @param boolean value to indicate timer should start
	# @param boolean value to perform status check on timer
	# @return amount of time left on countdown

	if duration['unit'] == 'min':
		seconds = duration['amount'] * 60
	if duration['unit']== 'h':
		seconds = duration['amount'] * 60 * 60
	else:
		seconds = duration['amount']
	time_dur = 0
	while time_dur != seconds and start != False:
		if status_check == True:
			status_check = False
			return time_dur
		print(time_dur)
		time.sleep(1)
		time_dur += 1
		queue.put({
			"widget": "timer",
			"widget_update":time_dur
			})