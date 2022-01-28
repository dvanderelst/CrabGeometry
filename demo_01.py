import pyCrab

crab = pyCrab.Crab()

crab.step(0,50)
crab.step(90, 100, update_estimation=False)
crab.step(90, 100, update_estimation=False)
crab.step(90, 150, update_estimation=False)
crab.step(90, 10, update_estimation=False)
crab.plot()