#!/usr/bin/env python

from wii_balance_board import Wiiboard, BoardEvent
import queue

def main():
	print("Board connexion test started!")
    
	# connect to balance board
	board = Wiiboard()
	#print "Discovering board..."
	address = board.discover()
    
	try:
		# Disconnect already-connected devices.
		# This is basically Linux black magic just to get the thing to work.
		subprocess.check_output(["bluez-test-input", "disconnect", address], stderr=subprocess.STDOUT)
		subprocess.check_output(["bluez-test-input", "disconnect", address], stderr=subprocess.STDOUT)
	except:
		pass
    
	print ("Trying to connect...")
	board.connect(address)  # The wii board must be in sync mode at this time
	board.wait(200)

	print(board.status)
    
	if board.status == "Connected":
		# Flash the LED so we know we can step on.
		board.setLight(False)
		board.wait(500)
		board.setLight(True)
    
		# start providing measurements
		print("start service")
		board.start_service()
		print("end service")

		print("set event")
		last_event = BoardEvent(1.0, 1.0, 1.0, 1.0, 0, 0)
	    
		# wait for player to step on board
		stepped_on = False
		good_count = 0
	
		print("start loop")
		while not stepped_on:
			# Flash the LED so we know we can step on.
			board.setLight(False)
			board.wait(500)
			board.setLight(True)
			try:
				event = board.EventQueue.get_nowait()
				qsize = board.EventQueue.qsize()
				for j in xrange(qsize):
					event2 = board.EventQueue.get()
					last_event = event
				if event.totalWeight > 20.0:
					good_count += 1
	            
			except queue.Empty:
				event = last_event
	        
			if good_count > 10:
				stepped_on = True

		print("loop ended")
	else:
		return



if __name__ == "__main__":
    main()