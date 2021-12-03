import pyCrab

crab = pyCrab.Crab()

crab.step(0, 100)
crab.step(-90, 30)
crab.step(-45, 0, update_estimation=False)
crab.print_states()
crab.plot()