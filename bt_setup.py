import bluetooth

def setup_bt():
	##
	# Function that discovers bt devices and pairs with them
	# Automates manual pairing and connection
	
	print("performing inquiry...")

	bt_device = "PLT V3200 Series"
	bt_addr = ""

	import bluetooth
	print("looking for nearby devices...")
	nearby_devices = bluetooth.discover_devices(lookup_names = True, flush_cache = True, duration = 5)
	print("found %d devices" % len(nearby_devices))
	for addr, name in nearby_devices:
		print(" %s - %s" % (addr, name))
		if name == bt_device:
			bt_addr = addr
			for services in bluetooth.find_service(address = addr):
				print(" Name: %s" % (services["name"]))
				print(" Description: %s" % (services["description"]))
				print(" Protocol: %s" % (services["protocol"]))
				print(" Provider: %s" % (services["provider"]))
				print(" Port: %s" % (services["port"]))
				print(" Service id: %s" % (services["service-id"]))

	print(bt_addr)
	client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
	client_socket.connect((bt_addr, 3))
	print("PLT V3200 Seris Connected")