import pyCrab

crab = pyCrab.Crab()

crab.step(0, 100)

crab.move(dy=100, rotation=0, update_estimation=False)
crab.step(0, 100)
crab.print_states()
crab.plot(aspect_equal=False)