def ncas_sonic_3_time(df):
   import time
   from datetime import datetime
   import calendar
   import numpy as np
   
   DT = []
   ET = []
   DoY = []
   
   header = df.columns
   #parse time
   ds = df.loc[:,header[0]:header[0]:1].values #extract date from data frame column 1
   for i in range(0, len(ds)):
      try: 
         tt = time.strptime(str(ds[i]), "['%Y-%m-%d %H:%M']")
      except:
         tt = time.strptime(str(ds[i]), "['%Y-%m-%d %H:%M:%S']")
      
      #DT
      DT.append(tt[0:6])
      #Doy
      DoY.append(float(tt[7]) + ((((float(tt[5])/60) + float(tt[4]))/60) + float(tt[3]))/24) 
      #ET
      ET.append(int(calendar.timegm(tt)))
      
   DT = np.array(DT)
   ET = np.array(ET)
   DoY = np.array(DoY)

   return DT, ET, DoY

def ncas_sonic_3_QC(df):
   import numpy as np
   
   header = df.columns
   
   DD = np.array(df.loc[:,header[1]:header[1]:1])
   FF = np.array(df.loc[:,header[2]:header[2]:1])
   
   DD = np.array(DD)
   FF = np.array(FF)
   WS = np.empty_like(FF)
   WS = WS.astype("float32")
   WD = np.empty_like(DD)
   WD = WD.astype("float32")
   
   for n in range(len(WS)):
      #Convert strings to numbers, replace with nan if there is a problem
      try:
         WS[n] = np.float32(FF[n])
      except:
         WS[n] = np.nan
         WD[n] = np.nan
         
      try:
         WD[n] = np.float32(DD[n])
      except:
         WD[n] = np.nan
         WS[n] = np.nan
      
      #WS < 0
      if np.isnan(WS[n]) == False:
         if WS[n] < 0:
            WD[n] = np.nan
            WS[n] = np.nan
         
      #WD < 0
      if np.isnan(WD[n]) == False:
         if WD[n] < 0:
            WD[n] = np.nan
            WS[n] = np.nan
      
      #WD > 360
      if np.isnan(WD[n]) == False:
         if WD[n] > 360:
            WD[n] = np.nan
            WS[n] = np.nan      
  
   return WS, WD

def ncas_sonic_3_means(DT, ET, DoY, WS, WD, data):
   import numpy as np
   import time
   from datetime import datetime
   import calendar 

   DT_m = []
   ET_m = []
   DoY_m = []
   WS_m = []
   WD_m = []
   WS_std = []
   WD_std = []
   U_m = []
   U_std = []
   V_m = []
   V_std = []
   
   for hr in range(24):
      for mn in range (60):
         ix = np.array(np.where((DT[:,3] == hr) & (DT[:,4] == mn)))
         ixs = ix.shape
         if ixs[1] > 1:
            #time
            tt_m = []
            tt_m.append(DT[ix[0,0],0])
            tt_m.append(DT[ix[0,0],1])
            tt_m.append(DT[ix[0,0],2])
            tt_m.append(hr)
            tt_m.append(mn)
            tt_m.append(0)
            tt_m.append(9999)
            tt_m.append(np.int32(DoY[0]))
            
            #DoY
            DoY_m.append(np.float32(tt_m[7]) + ((((np.float32(tt_m[5])/60) + np.float32(tt_m[4]))/60) + np.float32(tt_m[3]))/24) 
            #ET
            ET_m.append(int(calendar.timegm(tt_m)))
            #DT
            DT_m.append(tt_m[0:6])
           
            # spearate into components        
            ssa = []
            cca = []
            uu = []
            vv = []
            dd = np.array(WD[ix])
            #dd = dd.astype("float64")
            ff = np.array(WS[ix])
            #ff = ff.astype("float64")
            
            for n in range(ixs[1]):
               d = dd[0,n,0]
               f = ff[0,n,0]
               uu.append((-1) * f * np.sin(d * np.pi/180))
               vv.append((-1) * f * np.cos(d * np.pi/180))
               ssa.append(np.sin(d * np.pi/180))
               cca.append(np.cos(d * np.pi/180))
                           
            u = np.nanmean(np.array(uu))
            v = np.nanmean(np.array(vv))
            sa = np.nanmean(np.array(ssa))
            ca = np.nanmean(np.array(cca))
            
            U_m.append(np.nanmean(np.array(uu)))
            V_m.append(np.nanmean(np.array(vv)))
            U_std.append(np.nanstd(np.array(uu)))
            V_std.append(np.nanstd(np.array(vv)))
            
            #mean wind speed
            WS_m.append(np.sqrt((u * u) + (v * v)))
            #standard deviation wind speed
            WS_std.append(np.nanstd(np.array(np.float32(WS[ix]))))
            
            #mean wind direction
            WD_m.append((np.arctan2(u, v) * 180/np.pi) + 180)
            #standard deviation wind direction  Yamartino method        
            eta = np.sqrt(1 - ((ca * ca) + (sa * sa)))
            Z = (2/np.sqrt(3)) - 1
            Y = 1 + Z * (eta * eta * eta)
            X = np.arcsin(eta) * Y
            WD_std.append(X * 180/np.pi)
   
   DT_m = np.array(DT_m)
   ET_m = np.array(ET_m)
   DoY_m = np.array(DoY_m)  
   WS_m = np.array(WS_m)
   WD_m = np.array(WD_m)
   WS_std = np.array(WS_std)   
   WD_std = np.array(WD_std)  
   U_m = np.array(U_m)
   V_m = np.array(V_m)
   U_std = np.array(U_std)   
   V_std = np.array(V_std)  

   #remove nan
   for n in range(len(DoY_m)):
      if np.isnan(WS_m[n]) == True:
         WS_m[n] = -1e20
      if np.isnan(WS_std[n]) == True:
         WS_std[n] = -1e20  
      if np.isnan(WD_m[n]) == True:
         WD_m[n] = -1e20
      if np.isnan(WD_std[n]) == True:
         WD_std[n] = -1e20 
      if np.isnan(U_m[n]) == True:
         U_m[n] = -1e20
      if np.isnan(U_std[n]) == True:
         U_std[n] = -1e20  
      if np.isnan(V_m[n]) == True:
         V_m[n] = -1e20
      if np.isnan(V_std[n]) == True:
         V_std[n] = -1e20          
   
   #QC means, add flags, valid_min, valid_max, replace NaNs
   flag = np.ones_like(WS_m)
   
   #2 WS < 0
   ix = np.where((WS_m > -1e20) & (WS_m < 0))
   try:
      flag[ix] = 2
   except:
      pass
   #3 WS == 0
   ix = np.where(WS_m == 0)
   try:
      flag[ix] = 3
   except:
      pass
   #4 WS > 30 ms-1
   ix = np.where(WS_m > 30)
   try:
      flag[ix] = 4
   except:
      pass
   #5 WS missing
   ix = np.where(WS_m == -1e20)
   try:
      flag[ix] = 5
   except:
      pass
   #6 WD < 0
   ix = np.where((WD_m > -1e20) & (WD_m < 0))
   try:
      flag[ix] = 6
   except:
      pass
   #7 WD > 360
   ix = np.where(WD_m > 360)
   try:
      flag[ix] = 7
   except:
      pass
   #8 WD missing
   ix = np.where(WD_m == -1e20)
   try:
      flag[ix] = 8
   except:
      pass
   #9 U < -30
   ix = np.where((U_m > -1e20) & (U_m < -30))
   try:
      flag[ix] = 9
   except:
      pass
   #10 U > 30
   ix = np.where(U_m > 30)
   try:
      flag[ix] = 10
   except:
      pass
   #11 U == 0
   ix = np.where(U_m == 0)
   try:
      flag[ix] = 11
   except:
      pass
   #12 U missing
   ix = np.where(U_m == -1e20)
   try:
      flag[ix] = 12
   except:
      pass
   #13 V < -30
   ix = np.where((V_m > -1e20) & (V_m < -30))
   try:
      flag[ix] = 13
   except:
      pass
   #14 V > 30
   ix = np.where(V_m > 30)
   try:
      flag[ix] = 14
   except:
      pass
   #15 V == 0
   ix = np.where(V_m == 0)
   try:
      flag[ix] = 15
   except:
      pass
   #16 V missing
   ix = np.where(V_m == -1e20)
   try:
      flag[ix] = 16
   except:
      pass
   
   # valid min and max    
   ix = np.where(flag == 1)
   WS_m_min = np.min(WS_m[ix])
   WS_m_max = np.max(WS_m[ix])
   WS_std_min = np.min(WS_std[ix])
   WS_std_max = np.max(WS_std[ix])
   WD_m_min = np.min(WD_m[ix])
   WD_m_max = np.max(WD_m[ix])
   WD_std_min = np.min(WD_std[ix])
   WD_std_max = np.max(WD_std[ix])
   U_m_min = np.min(U_m[ix])
   U_m_max = np.max(U_m[ix])
   U_std_min = np.min(U_std[ix])
   U_std_max = np.max(U_std[ix])
   V_m_min = np.min(V_m[ix])
   V_m_max = np.max(V_m[ix])
   V_std_min = np.min(V_std[ix])
   V_std_max = np.max(V_std[ix])
   
   data.ET = np.array(ET_m)
   data.DoY = np.array(DoY_m)
   data.DT = np.array(DT_m)
   data.WS_mean = np.array(WS_m)
   data.WS_std = np.array(WS_std)
   data.WD_mean = np.array(WD_m)
   data.WD_std = np.array(WS_std)
   data.U_mean = np.array(U_m)
   data.U_std = np.array(U_std)
   data.V_mean = np.array(V_m)
   data.V_std = np.array(V_std)   
   data.flag = np.array(flag)
   data.WS_m_min = WS_m_min
   data.WS_m_max = WS_m_max
   data.WS_std_min = WS_std_min
   data.WS_std_max = WS_std_max
   data.WD_m_min = WD_m_min
   data.WD_m_max = WD_m_max 
   data.WD_std_min = WD_std_min
   data.WD_std_max = WD_std_max
   data.U_m_min = U_m_min
   data.U_m_max = U_m_max
   data.U_std_min = U_std_min
   data.U_std_max = U_std_max
   data.V_m_min = V_m_min
   data.V_m_max = V_m_max
   data.V_std_min = V_std_min
   data.V_std_max = V_std_max
   
   return data

def ncas_sonic_3(fn_in, data, logfile): 
   import pandas as pd  
   
   try:
      df = pd.read_csv(fn_in, usecols=[0,3,4], header=None)
   except:
      # exit if problem encountered
      print("Unable to open data file: ", fn_in, ". This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open data file: ' + fn_in + 'Program will terminate.\n')
      g.close()
      exit()
   #parse file times   
   [DT, ET, DoY] = ncas_sonic_3_time(df)
   #parse and QC raw wind data
   [WS, WD] = ncas_sonic_3_QC(df)
   
   #1 minute means
   data = ncas_sonic_3_means(DT, ET, DoY, WS, WD, data)
    
   return data    
         
def ncas_aws_3_time(df, data):
   import time
   from datetime import datetime
   import calendar
   import numpy as np
   
   DT = []
   ET = []
   DoY = []
   
   header = df.columns
   #parse time
   ds = df.loc[:,header[0]:header[0]:1].values #extract date from data frame column 1

   for i in range(0, len(ds)):
      try: 
         tt = time.strptime(str(ds[i]), "['%Y-%m-%d %H:%M']")
      except:
         tt = time.strptime(str(ds[i]), "['%Y-%m-%d %H:%M:%S']")
      
      #DT
      DT.append(tt[0:6])
      #Doy
      DoY.append(float(tt[7]) + ((((float(tt[5])/60) + float(tt[4]))/60) + float(tt[3]))/24) 
      #ET
      ET.append(int(calendar.timegm(tt)))
      
   data.DT = np.array(DT)
   data.ET = np.array(ET)
   data.DoY = np.array(DoY)
 
   return data
   
def ncas_aws_3_QC(df, data):
   import numpy as np  

   header = df.columns
   
   #Temperature
   X = np.array(df.loc[:,header[1]:header[1]:1])
   TT = np.empty_like(X)
   for n in range(len(TT)):
      try:
         TT[n] = np.fromstring(X[n], dtype=float)
      except:
         TT[n] = np.nan
   del X
  
   #Humidity
   X = np.array(df.loc[:,header[2]:header[2]:1])
   RH = np.empty_like(X)
   for n in range(len(RH)):
      try:
         RH[n] = np.fromstring(X[n], dtype=float)
      except:
         RH[n] = np.nan
   del X      
   
   #Wind speed
   X = np.array(df.loc[:,header[3]:header[3]:1])
   WS = np.empty_like(X)
   for n in range(len(WS)):
      try:
         WS[n] = np.fromstring(X[n], dtype=float)
      except:
         WS[n] = np.nan
   del X 
   
   #Wind direction
   X = np.array(df.loc[:,header[4]:header[4]:1])
   WD = np.empty_like(X)
   for n in range(len(WD)):
      try:
         WD[n] = np.fromstring(X[n], dtype=float)
      except:
         WD[n] = np.nan
   del X
   
   #Accumulated rain
   X = np.array(df.loc[:,header[5]:header[5]:1])
   PA = np.empty_like(X)
   for n in range(len(PA)):
      try:
         PA[n] = np.fromstring(X[n], dtype=float)
      except:
         PA[n] = np.nan
   del X
   
   #Rain rate
   X = np.array(df.loc[:,header[6]:header[6]:1])
   PR = np.empty_like(X)
   for n in range(len(PR)):
      try:
         PR[n] = np.fromstring(X[n], dtype=float)
      except:
         PR[n] = np.nan
   del X

   #pressure
   X = np.array(df.loc[:,header[7]:header[7]:1])
   PP = np.empty_like(X)
   for n in range(len(PP)):
      try:
         PP[n] = (np.fromstring(X[n], dtype=float))/10000
      except:
         PP[n] = np.nan
   del X
   
   #Solar
   X = np.array(df.loc[:,header[8]:header[8]:1])
   SL = np.empty_like(X)
   for n in range(len(SL)):
      try:
         SL[n] = (np.fromstring(X[n], dtype=float))
      except:
         SL[n] = np.nan
   del X
   
   #UV
   X = np.array(df.loc[:,header[9]:header[9]:1])
   UV = np.empty_like(X)
   for n in range(len(SL)):
      try:
         UV[n] = (np.fromstring(X[n], dtype=float))
      except:
         UV[n] = np.nan
   del X
   
   # remove nans
   for n in range(len(data.DoY)):
      if np.isnan(TT[n]) == True:
         TT[n] = -1e20
      if np.isnan(RH[n]) == True:
         RH[n] = -1e20  
      if np.isnan(WS[n]) == True:
         WS[n] = -1e20
      if np.isnan(WD[n]) == True:
         WD[n] = -1e20 
      if np.isnan(PP[n]) == True:
         PP[n] = -1e20
      if np.isnan(PA[n]) == True:
         PA[n] = -1e20  
      if np.isnan(PR[n]) == True:
         PR[n] = -1e20
      if np.isnan(SL[n]) == True:
         SL[n] = -1e20 
      if np.isnan(UV[n]) == True:
         UV[n] = -1e20     
   
   # create flags
   # Temperature
   qc_flag_temperature = np.ones_like(TT)
   #T>30 2b
   ix = np.where(TT > 30)
   try:
      qc_flag_temperature[ix] = 2
   except:
      pass
   
   #T>40 3b
   ix = np.where(TT > 40)
   try:
      qc_flag_temperature[ix] = 3
   except:
      pass
      
   #T<-10 4b
   ix = np.where((TT > -1e20) & (TT < -10))
   try:
      qc_flag_temperature[ix] = 4
   except:
      pass
   
   #T<-20 5b
   ix = np.where((TT > -1e20) & (TT < -20))
   try:
      qc_flag_temperature[ix] = 5
   except:
      pass
      
   #Missing 6b
   ix = np.where(TT == -1e20)
   try:
      qc_flag_temperature[ix] = 6
   except:
      pass
      
   #Humidity
   qc_flag_relative_humidity = np.ones_like(RH)
   #RH>100 2b
   ix = np.where(RH > 100)
   try:
      qc_flag_relative_humidity[ix] = 2
   except:
      pass
   
   #RH == 100 3b
   ix = np.where(RH == 100)
   try:
      qc_flag_relative_humidity[ix] = 3
   except:
      pass
      
   #RH<40 4b
   ix = np.where(RH < 40)
   try:
      qc_flag_relative_humidity[ix] = 4
   except:
      pass
   
   #RH<0 5b
   ix = np.where(RH < 0)
   try:
      qc_flag_relative_humidity[ix] = 5
   except:
      pass
   
   #Missing 6b
   ix = np.where(RH == -1e20)
   try:
      qc_flag_relative_humidity[ix] = 6
   except:
      pass
   
   # Presure
   qc_flag_pressure = np.ones_like(PP)
   #PP>1000 2b
   ix = np.where(PP > 1000)
   try:
      qc_flag_pressure[ix] = 2
   except:
      pass
      
   #PP>1100 3b
   ix = np.where(PP > 1100)
   try:
      qc_flag_pressure[ix] = 3
   except:
      pass
      
   #PP<950 4b
   ix = np.where(PP < 950)
   try:
      qc_flag_pressure[ix] = 4
   except:
      pass
   
   #PP<0 5b
   ix = np.where(PP < 0)
   try:
      qc_flag_pressure[ix] = 5
   except:
      pass
   
   #Missing 6b
   ix = np.where(PP == -1e20)
   try:
      qc_flag_pressure[ix] = 6
   except:
      pass
      
   #wind speed   
   qc_flag_wind_speed = np.ones_like(WS)
   #WS>30 2b
   ix = np.where(WS > 30)
   try:
      qc_flag_wind_speed[ix] = 2
   except:
      pass
  
   #WS=0 3b
   ix = np.where(WS == 0)
   try:
      qc_flag_wind_speed[ix] = 3
   except:
      pass
  
   #WS<0 4b
   ix = np.where(WS < 0)
   try:
      qc_flag_wind_speed[ix] = 4
   except:
      pass
  
   #Missing 5b
   ix = np.where(WS == -1e20)
   try:
      qc_flag_wind_speed[ix] = 5
   except:
      pass
   
   #wind direction
   qc_flag_wind_from_direction = np.ones_like(WD)
   #WD>360 2b
   ix = np.where(WD > 360)
   try:
      qc_flag_wind_from_direction[ix] = 2
   except:
      pass
      
   #WD<0 3b
   ix = np.where(WD < 0)
   try:
      qc_flag_wind_from_direction[ix] = 3
   except:
      pass
   
   #WS == 0 4b
   ix = np.where(WS == 0)
   try:
      qc_flag_wind_from_direction[ix] = 4
   except:
      pass
      
   #Missing 5b
   ix = np.where(WD == -1e20)
   try:
      qc_flag_wind_from_direction[ix] = 5
   except:
      pass
   
   #radiation
   qc_flag_radiation = np.ones_like(UV)
   #UV>2000 2b
   ix = np.where(UV > 2000)
   try:
      qc_flag_radiation[ix] = 2
   except:
      pass
      
   #UV<0 3b
   ix = np.where(UV < 0)
   try:
      qc_flag_radiation[ix] = 3
   except:
      pass
      
   #Missing UV 4b
   ix = np.where(UV == -1e20)
   try:
      qc_flag_radiation[ix] = 4
   except:
      pass
   
   #SL>2000 5b
   ix = np.where(SL > 2000)
   try:
      qc_flag_radiation[ix] = 5
   except:
      pass
      
   #SL<0 6b
   ix = np.where(SL < 0)
   try:
      qc_flag_radiation[ix] = 6
   except:
      pass
      
   #Missing SL 7b
   ix = np.where(SL == -1e20)
   try:
      qc_flag_radiation[ix] = 7
   except:
      pass
   
   #precipitation
   qc_flag_precipitation = np.ones_like(PA)
   #PA>25 2b  300 *(5/60)
   ix = np.where(PA > 25)
   try:
      qc_flag_precipitation[ix] = 2
   except:
      pass
      
   #PA<0 3b
   ix = np.where(PA < 0)
   try:
      qc_flag_precipitation[ix] = 3
   except:
      pass
   
   #Missing PA 4b
   ix = np.where(PA == -1e20)
   try:
      qc_flag_precipitation[ix] = 4
   except:
      pass
   
   #PR>300 5b
   ix = np.where(PR > 300)
   try:
      qc_flag_precipitation[ix] = 5
   except:
      pass
      
   #PR<0 6b
   ix = np.where(PR < 0)
   try:
      qc_flag_precipitation[ix] = 6
   except:
      pass
   
   #Missing PR 7b
   ix = np.where(PR == -1e20)
   try:
      qc_flag_precipitation[ix] = 7
   except:
      pass
   
   # min and max
   ix = np.where(qc_flag_temperature < 3 )
   TT_min = np.min(TT[ix])
   TT_max = np.max(TT[ix])
   
   ix = np.where(qc_flag_relative_humidity == 1)
   RH_min = np.min(RH[ix])
   RH_max = np.max(RH[ix])
   
   ix = np.where(qc_flag_wind_speed == 1)
   WS_min = np.min(WS[ix])
   WS_max = np.max(WS[ix])
   
   ix = np.where(qc_flag_wind_from_direction == 1)
   WD_min = np.min(WD[ix])
   WD_max = np.max(WD[ix])
   
   ix = np.where(qc_flag_pressure < 4)
   PP_min = np.min(PP[ix])
   PP_max = np.max(PP[ix])
   
   ix = np.where(qc_flag_precipitation == 1)
   PA_min = np.min(PA[ix])
   PA_max = np.max(PA[ix])
   
   ix = np.where(qc_flag_precipitation == 1)
   PR_min = np.min(PR[ix])
   PR_max = np.max(PR[ix])
   
   ix = np.where(qc_flag_radiation == 1)
   SL_min = np.min(SL[ix])
   SL_max = np.max(SL[ix])
   
   ix = np.where(qc_flag_radiation == 1)
   UV_min = np.min(UV[ix])
   UV_max = np.max(UV[ix])
   
   #convert temperature to kelvin
   TT = TT + 273.15
   TT_min = TT_min + 273.15
   TT_max = TT_max + 273.15
   
   data.TT = TT
   data.TT_min = TT_min
   data.TT_max = TT_max
   data.RH = RH
   data.RH_min = RH_min
   data.RH_max = RH_max
   data.WS = WS
   data.WS_min = WS_min
   data.WS_max = WS_max
   data.WD = WD
   data.WD_min = WD_min
   data.WD_max = WD_max
   data.PP = PP
   data.PP_min = PP_min
   data.PP_max = PP_max
   data.PA = PA
   data.PA_min = PA_min
   data.PA_max = PA_max
   data.PR = PR
   data.PR_min = PR_min
   data.PR_max = PR_max
   data.SL = SL
   data.SL_min = SL_min
   data.SL_max = SL_max
   data.UV = UV
   data.UV_min = UV_min
   data.UV_max = UV_max
   data.qc_flag_temperature = qc_flag_temperature
   data.qc_flag_relative_humidity = qc_flag_relative_humidity
   data.qc_flag_pressure = qc_flag_pressure
   data.qc_flag_wind_speed = qc_flag_wind_speed
   data.qc_flag_wind_from_direction = qc_flag_wind_from_direction
   data.qc_flag_radiation = qc_flag_radiation
   data.qc_flag_precipitation = qc_flag_precipitation
   
   return data  

def ncas_aws_3(fn_in, data, logfile): 
   import pandas as pd  
  
   try:
      df = pd.read_csv(fn_in, usecols=[0,1,4,6,8,9,10,11,14,15])
   except:
      # exit if problem encountered
      print("Unable to open data file: ", fn_in, ". This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open data file: ' + fn_in + 'Program will terminate.\n')
      g.close()
      exit()
   
   #parse time
   data = ncas_aws_3_time(df, data)
   
   #parse_data
   data = ncas_aws_3_QC(df, data)
   
   return data 