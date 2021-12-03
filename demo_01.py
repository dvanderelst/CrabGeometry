import pyCrab

crab = pyCrab.Crab()

crab.step(90, 100)
crab.step(90, 100)
crab.step(90, 100, update_estimation=False)
crab.plot()