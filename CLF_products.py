def create_NC_file(nm, dp, ver, opt1, opt2, opt3, start_date, logfile):
   from netCDF4 import Dataset
   from datetime import datetime
   
   try:
      # create nc file
      from netCDF4 import Dataset
      dout = 'Data\\'
      f1 = nm # instrument name
      f2 = 'north-kensington'
      f3 = datetime.fromtimestamp(int(start_date)).strftime('%Y%m%d') # date
      f4 = dp # data product
      f5 = 'v' + ver # version number
      f6 = '.nc'
      
      if ((len(opt1)<1) and (len(opt2)<1) and (len(opt3)<1)):
         fn = dout+f1+chr(95)+f2+chr(95)+f3+chr(95)+f4+chr(95)+f5+f6         
      if ((len(opt1)>1) and (len(opt2)<1) and (len(opt3)<1)):
         fn = dout+f1+chr(95)+f2+chr(95)+f3+chr(95)+f4+chr(95)+opt1+chr(95)+f5+f6
      if ((len(opt1)>1) and (len(opt2)>1) and (len(opt3)<1)):
         fn = dout+f1+chr(95)+f2+chr(95)+f3+chr(95)+f4+chr(95)+opt1+chr(95)+opt2+chr(95)+f5+f6
      if ((len(opt1)>1) and (len(opt2)>1) and (len(opt3)>1)):
         fn = dout+f1+chr(95)+f2+chr(95)+f3+chr(95)+f4+chr(95)+opt1+chr(95)+opt2+chr(95)+opt3+chr(95)+f5+f6
      
      nc = Dataset(fn, "w",  format = "NETCDF4_CLASSIC") 
   except:
      # exit if problem encountered
      print('Unable to create: ',fn,'. This program will terminate')
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat()+' Unable to create: '+fn+'. This program will terminate\n')
      g.close()
      exit()
      
      del Dataset, datetime

   return nc

# A
# B
# C   
# D   
# E
# F
# G
# H
# I
# J
# K
# L
# M
def mean_winds(meta, data, nc):
   import CLF_common as com
   import numpy as np
   
   # write common global attrib 
   com.global_attributes(nc, meta, data.ET)
      
   # write common dimensions
   com.dimensions(nc, data.ET)
   
   # write common variables
   com.variables(nc, data)  
   
   v = nc.createVariable('wind_speed', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'm s-1'
   v.standard_name = 'wind_speed'
   v.long_name = 'Mean Wind Speed'
   v.valid_min = np.float32(data.WS_m_min)
   v.valid_max = np.float32(data.WS_m_max)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.WS_mean)
   
   v = nc.createVariable('wind_from_direction', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'degree'
   v.standard_name = 'wind_from_direction'
   v.long_name = 'Wind From Direction'
   v.valid_min = np.float32(data.WD_m_min)
   v.valid_max = np.float32(data.WD_m_max)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.WD_mean)
   
   v = nc.createVariable('eastward_wind', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'm s-1'
   v.standard_name = 'eastward_wind'
   v.long_name = 'Eastward Wind Component (U)'
   v.valid_min = np.float32(data.U_m_min)
   v.valid_max = np.float32(data.U_m_max)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.U_mean)

   v = nc.createVariable('northward_wind', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'm s-1'
   v.standard_name = 'northward_wind'
   v.long_name = 'Northward Wind Component (V)'
   v.valid_min = np.float32(data.V_m_min)
   v.valid_max = np.float32(data.V_m_max)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.V_mean)
   
   v = nc.createVariable('divergence_of_wind', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'm s-1'
   v.standard_name = 'divergence_of_wind'
   v.long_name = 'Divergence of Horizontal Winds Speed'
   v.valid_min = np.float32(data.WS_std_min)
   v.valid_max = np.float32(data.WS_std_max)
   v.cell_methods = 'time: standard_deviation'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.WS_std)
   
   v = nc.createVariable('divergence_of_wind_from_direction', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'degree'
   v.long_name = 'Divergence of Wind from Direction'
   v.valid_min = np.float32(data.WD_std_min)
   v.valid_max = np.float32(data.WD_std_max)
   v.cell_methods = 'time: standard_deviation'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.WD_std)
   
   v = nc.createVariable('divergence_of_eastward_wind', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'm s-1'
   v.long_name = 'Divergence of Eastward Wind Component (Sigma U)'
   v.valid_min = np.float32(data.U_std_min)
   v.valid_max = np.float32(data.U_std_max)
   v.cell_methods = 'time: standard_deviation'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.U_std)
   
   v = nc.createVariable('divergence_of_northward_wind', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'm s-1'
   v.long_name = 'Divergence of Northward Wind Component (Sigma V)'
   v.valid_min = np.float32(data.V_std_min)
   v.valid_max = np.float32(data.V_std_max)
   v.cell_methods = 'time: standard_deviation'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.V_std)
   
   #2 WS < 0
   #3 WS == 0
   #4 WS > 30 ms-1
   #5 WS missing
   #6 WD < 0
   #7 WD > 360
   #8 WD missing
   #9 U < -30
   #10 U > 30
   #11 U == 0
   #12 U missing
   #13 V < -30
   #14 V > 30
   #15 V == 0
   #16 V missing
   
   v = nc.createVariable('qc_flag', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag'
   v.flag_values = '0b,1b,2b,3b,4b,5b,6b,7b,8b,9b,10b,11b,12b,13b,14b,15b,16b'
   v.flag_meanings = '0b:not_used' + '\n'
   v.flag_meanings = v.flag_meanings + '1b:good_data' + '\n'
   v.flag_meanings = v.flag_meanings + '2b:suspect_data_data:_mean_wind_speed<0_ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + '3b:suspect_data_data:_mean_wind_speed=0_ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + '4b:suspect_data_data:_mean_wind_speed>30_ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + '5b:bad_data_do_not_use:_mean_wind_speed_missing_data' + '\n'
   v.flag_meanings = v.flag_meanings + '6b:suspect_data_data:_mean_wind_direction<0_degrees' + '\n'
   v.flag_meanings = v.flag_meanings + '7b:suspect_data_data:_mean_wind_direction>360_degrees' + '\n'
   v.flag_meanings = v.flag_meanings + '8b:bad_data_do_not_use:_mean_wind_direction_missing_data' + '\n'
   v.flag_meanings = v.flag_meanings + '9b:suspect_data_data:_U_component<-30_ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + '10b:suspect_data_data:_U_component>30_ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + '11b:suspect_data_data:_U_component=0_ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + '12b:bad_data_do_not_use:_U_component_missing_data' + '\n'
   v.flag_meanings = v.flag_meanings + '13b:suspect_data_data:_V_component<-30_ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + '14b:suspect_data_data:_V_component>30_ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + '15b:suspect_data_data:_V_component=0_ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + '16b:bad_data_do_not_use:_V_component_missing_data' 
   #write data
   v[:] = np.int8(data.flag)
     
# N
# O   
# P
# Q
# R
# S
def surface_met(meta, data, nc, ver):
   #metpak
   import CLF_common as com
   import numpy as np
   
   # write common global attrib 
   com.global_attributes(nc, meta, data.ET)
   
   # write specific global attrib
   nc.product_version = ver
      
   # write common dimensions
   com.dimensions(nc, data.ET)
   
   # write common variables
   com.variables(nc, data)
   
   # write specific variables
   v = nc.createVariable('air_pressure', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'hPa'
   v.standard_name = 'air_pressure'
   v.long_name = 'Air Pressure'
   v.valid_min = np.float32(data.min_dat7)
   v.valid_max = np.float32(data.max_dat7)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.PP) 
   
   v = nc.createVariable('air_temperature', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'K'
   v.standard_name = 'air_temperature'
   v.long_name = 'Air Temperature'
   v.valid_min = np.float32(data.min_dat2)
   v.valid_max = np.float32(data.max_dat2)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.TT)
   
   v = nc.createVariable('relative_humidity', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = '%'
   v.standard_name = 'relative_humidity'
   v.long_name = 'Relative Humidity'
   v.valid_min = np.float32(data.min_dat1)
   v.valid_max = np.float32(data.max_dat1)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.RH)
   
   v = nc.createVariable('wind_speed', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'm s-1'
   v.standard_name = 'wind_speed'
   v.long_name = 'Wind Speed'
   v.valid_min = np.float32(data.min_dat5)
   v.valid_max = np.float32(data.max_dat5)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.WS)
   
   v = nc.createVariable('wind_from_direction', np.float32, ('time',), fill_value=-1.00e+20)
   #variable attributes
   v.units = 'degree'
   v.standard_name = 'wind_from_direction'
   v.long_name = 'Wind From Direction'
   v.valid_min = np.float32(data.min_dat6)
   v.valid_max = np.float32(data.max_dat6)
   v.cell_methods = 'time: mean'
   v.coordinates = 'latitude longitude'
   #write data
   v[:] = np.float32(data.WD)
   
   v = nc.createVariable('qc_flag_temperature', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: Temperature'
   v.flag_values = '0b,1b,2b,3b,4b,5b,6b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data_below_measurement_threshold_of_50C' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data_above_measurement_threshold_of_100C' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data:T<_-20C_and_T>-50C' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data:T>_40C_and_T<100C' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(data.flag2)  
   
   v = nc.createVariable('qc_flag_relative_humidity', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: Relative Humidity'
   v.flag_values = '0b,1b,2b,3b,4b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data_below_measurement_threshold_of_0%' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data_above_measurement_threshold_of_100%' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(data.flag1)
   
   v = nc.createVariable('qc_flag_pressure', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: Pressure'
   v.flag_values = '0b,1b,2b,3b,4b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data_below_measurement_threshold_of_600hPa' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data_above_measurement_threshold_of_11000hPa' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(data.flag7)
   
   v = nc.createVariable('qc_flag_wind_speed', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: Wind Speed'
   v.flag_values = '0b,1b,2b,3b,4b,5b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data_below_measurement_threshold_of_0ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data_above_measurement_threshold_of_60ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data:data=0ms-1' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(data.flag5)
   
   v = nc.createVariable('qc_flag_wind_from_direction', np.int8, ('time',))
   #variable attribute
   v.units = '1'
   v.long_name = 'Data Quality Flag: Wind From Direction'
   v.flag_values = '0b,1b,2b,3b,4b,5b'
   v.flag_meanings = 'not_used' + '\n'
   v.flag_meanings = v.flag_meanings + 'good_data' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data_below_measurement_threshold_of_0degrees' + '\n'
   v.flag_meanings = v.flag_meanings + 'bad_data_do_not_use:data_above_measurement_threshold_of_359degrees' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data:windspeed=0ms-1_so_direction_cannot_be_determined' + '\n'
   v.flag_meanings = v.flag_meanings + 'suspect_data_time_stamp_error' 
   #write data
   v[:] = np.int8(data.flag6)  