import pyCrab

#%%
crab = pyCrab.Crab()

crab.step(0, 100)
crab.move(rotation=35, update_estimation=False)
crab.plot(aspect_equal=True)
#%%

crab = pyCrab.Crab()
crab.step(0, 50)
crab.step(rotation=-35, distance=50)
crab.step(rotation= 35, update_estimation=False)
crab.plot(aspect_equal=True)
print(crab.real_frame.history)
#%%
crab = pyCrab.Crab()

proportion = 1

crab.step(0, 100)
crab.step(rotation=-90, distance=0, update_estimation=False)
crab.update_estimation(rotation=-90 * proportion)

crab.step(distance=50)
crab.step(rotation= 35, update_estimation=False)
crab.plot(aspect_equal=True)
print(crab.real_frame.history)