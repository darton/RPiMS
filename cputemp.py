
cpu = CPUTemperature()
#print('CPU temperature: {}C'.format(cpu.temperature))
redis_db.set('CPUtemperature', cpu.temperature)
