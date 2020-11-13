def global_attributes(nc, meta, ET):
   from datetime import datetime
  
   for x in range(0,len(meta[:,0])):
      nc.setncattr(meta[x,0], meta[x,1])
   
   # write specific global attribute
   nc.last_revised_date = datetime.utcnow().isoformat()  
   nc.time_coverage_start = datetime.utcfromtimestamp(ET[0]).isoformat()
   nc.time_coverage_end = datetime.utcfromtimestamp(ET[len(ET)-1]).isoformat()
   del datetime
      
def dimensions(nc, ET):
   time = nc.createDimension('time', len(ET))
   latitude = nc.createDimension('latitude', 1)
   longitude = nc.createDimension('longitude', 1)
   
def variables(nc, data):
   import numpy as np
   
   #time
   v = nc.createVariable('time', np.float64, ('time',))
   #variable attributes
   v.units = 'seconds since 1970-01-01 00:00:00'
   v.standard_name = 'time'
   v.long_name = 'Time (seconds since 1970-01-01 00:00:00)'
   v.axis = 'T'
   v.valid_min = np.float64(min(data.ET))
   v.valid_max = np.float64(max(data.ET))
   v.calendar = 'standard'
   #write data
   v[:] = np.float64(data.ET)

   #lat
   v = nc.createVariable('latitude', np.float32, ('latitude',))
   #variable attributes
   v.units = 'degrees_north'
   v.standard_name = 'latitude'
   v.long_name = 'Latitude'
   #write data
   v[:] = np.float32(data.lat)
   
   #lon
   v = nc.createVariable('longitude', np.float32, ('longitude',))
   #variable attributes
   v.units = 'degrees_east'
   v.standard_name = 'longitude'
   v.long_name = 'Longitude'
   #write data
   v[:] = np.float32(data.lon)
   
   #doy
   v = nc.createVariable('day_of_year', np.float32, ('time',))
   #variable attributes
   v.units = '1'
   v.long_name = 'Day of Year'
   v.valid_min = np.float32(min(data.DoY))
   v.valid_max = np.float32(max(data.DoY))
   #write data
   v[:] = np.float32(data.DoY)
   
   #year
   v = nc.createVariable('year', np.int32, ('time',))
   #variable attributes
   v.units = '1'
   v.long_name = 'Year'
   v.valid_min = np.int32(min(data.DT[:,0]))
   v.valid_max = np.int32(max(data.DT[:,0])) 
   #write data
   v[:] = np.int32(data.DT[:,0])
   
   #month
   v = nc.createVariable('month', np.int32, ('time',))
   #variable attributes
   v.units = '1'
   v.long_name = 'Month'
   v.valid_min = np.int32(min(data.DT[:,1]))
   v.valid_max = np.int32(max(data.DT[:,1])) 
   #write data
   v[:] = np.int32(data.DT[:,1])
   
   #day
   v = nc.createVariable('day', np.int32, ('time',))
   #variable attributes
   v.units = '1'
   v.long_name = 'Day'
   v.valid_min = np.int32(min(data.DT[:,2]))
   v.valid_max = np.int32(max(data.DT[:,2]))
   #write data
   v[:] = np.int32(data.DT[:,2])
   
   #hour
   v = nc.createVariable('hour', np.int32, ('time',))
   #variable attributes
   v.units = '1'
   v.long_name = 'Hour'
   v.valid_min = np.int32(min(data.DT[:,3]))
   v.valid_max = np.int32(max(data.DT[:,3])) 
   #write data
   v[:] = np.int32(data.DT[:,3])
   
   #minute
   v = nc.createVariable('minute', np.int32, ('time',))
   #variable attributes
   v.units = '1'
   v.long_name = 'Minute'
   v.valid_min = np.int32(min(data.DT[:,4]))
   v.valid_max = np.int32(max(data.DT[:,4]))  
   #write data
   v[:] = np.int32(data.DT[:,4])
   
   #second
   v = nc.createVariable('second', np.float32, ('time',))
   #variable attributes
   v.units = '1'
   v.long_name = 'Second'
   v.valid_min = np.float32(min(data.DT[:,5]))
   v.valid_max = np.float32(max(data.DT[:,5])) 
   #write data
   v[:] = np.float32(data.DT[:,5])
   
   del np