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
      df = pd.read_csv(fn_in, usecols=[0,3,4])
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
         
#def ncas_aws_3(fn_in, data, logfile): 
#   return data 