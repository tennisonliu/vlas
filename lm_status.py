def get_lm_status(lab_machine_status, lab_machine, queue):
	##
	# Function that polls lab machine status and returns whether
	# it is on or off
	# @param lab_machine_status: dictionary structure tracking the status of all lab machines
	# @param lab_machine: name of exact machine to query
	# @param queue: queue used to update GUI thread
	
	lm_status_query = lab_machine_status[lab_machine]
	if lm_status_query == True:
		lm_status_query = "on"
	else:
		lm_status_query = "off"
	queue.put({
		"widget": "conv_hist", 
		"widget_update" : "CsiroBot: " + lab_machine + " is turned " + lm_status_query
		})