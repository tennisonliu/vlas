from pymodbus.client.sync import ModbusTcpClient
import serial.tools.list_ports as portlist


# NOTE: set local machine's IP address so that it is in the 
# same subnet as the moxa controller. Use two different network
# cards?

def control_equipment(machine, action, queue):
	##
	# Function that controls machinery connected to the MOXA device
	# by turning them on and off
	# @param machine: name of machine to be interfaced
	# @param action: action to be performed on machine [on, off]
	# @param queue: queue used to update GUI thread

	lab_machine = {
		"Lab Machine One": 0,
		"Lab Machine Two": 1,
		"Lab Machine Three": 2,
		"Lab Machine Four": 3
	}
	client = ModbusTcpClient('192.168.127.254')
	if action == "on":
		client.write_coil(lab_machine['machine'], True)
		result = client.read_coils(lab_machine['machine'], 1)
		if result.bits[0]!=True:
			raise ValueError("Incorrect command")
	if action == "off":
		client.write_coil(lab_machine['machine'], False)
		result = client.read_coils(lab_machine['machine'], 1)
		if result.bits[0]!=False:
			raise ValueError("Incorrect command")


	queue.put({
		"widget": "conv_hist",
		"widget_update" : "CsiroBot: Lab Machine Three activated."
		})
	queue.put({
		"widget": "lm_control",
		"widget_update": str(lab_machine['machine']+1)+str(True)
		})

	client.close()