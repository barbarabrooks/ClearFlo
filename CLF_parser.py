def read_meta(logfile, name):
   import pandas as pd
   import numpy as np
   from datetime import datetime
   
   # read in meta
   try:
      df = pd.read_excel("meta.xlsx")
   except:
      # exit if problem encountered
      print("Unable to open meta.xlsx. This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open meta.xlsx. Program will terminate.\n')
      g.close()
      exit()     
      
   # find the approprate line
   inst = df.loc[:, 'instrument\n':'instrument\n':1].values
   tp = df.columns
   header = np.array(tp[1:len(tp)])      
   for x in range (0, len(inst)):
      if (name in inst[x]):
         tp = df.loc[x,:].values  
         dd = np.array(tp[1:len(tp)])
         break
            
   meta = np.empty([len(header), 2], dtype=object)       
   if 'dd' not in locals():
      print("Can't find meta data about named instrument. This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Can\'t find meta data about named instrument. Program will terminate.\n')
      g.close()
      exit()
   else:
      for x in range (0, len(header)):
         meta[x, 0] = header[x]
         meta[x, 1] = dd[x]
   
   del pd, datetime, np    
   
   return meta

def read_config(logfile):
   from datetime import datetime
   import numpy as np
   
   # read in Config file
   try:
      f = open("Config.txt", "r")
      if f.mode == 'r':
         lines = f.readlines()
         f.close()
   except:
      # exit if problem encountered
      print("Unable to open Config.txt file. This program will terminate")
      g = open(logfile, 'a')
      g.write(datetime.utcnow().isoformat() + ' Unable to open Config.txt. Program will terminate.\n')
      g.close()
      exit()
   
   # process information in config file
   x_st = 0; x_ed = 0;
   ss1 = "Start - do not remove"
   for x in range (0, len(lines)):
      if (ss1 in lines[x]):
         try:
            ver = lines[x+1].strip('\n') 
            name = lines[x+2].strip('\n') 
            product = lines[x+3].strip('\n') 
            fn_in =  lines[x+4].strip('\n')        
            break  
         except:   
            print("An instrument product pair must be given. This program will terminate.")
            g = open(logfile, 'a')
            g.write(datetime.utcnow().isoformat() + ' Error in config file. Program will terminate.\n')
            g.close()
            exit()
      
   del lines, datetime, np
      
   return ver, fn_in, name, product
      
def read_data_file(dp, fn_in, data, logfile):
   import CLF_data as dat
   
   if dp == 'ncas-sonic-3':
      data = dat.ncas_sonic_3(fn_in, data, logfile)
         
   #if dp == 'ncas-aws-3':
   #   data = dat.ncas_aws_3(fn_in, data, logfile)    
         
   del dat
   
   return data

def do_run(name, product, ver, meta, data, logfile):
   import CLF_products as prod
      
   start_date = ''
   # set default file naming options
   opt1 = ''; opt2 = ''; opt3 = ''
      
   # create, write and close the files
   # M
   if product == 'mean-winds':
      # create nc file
      nc = prod.create_NC_file(name, product, ver, opt1, opt2, opt3, data.ET[0], logfile)
      prod.mean_winds(meta, data, nc)
      nc.close()
         
   # S      
   if product == 'surface-met':
      # create nc file - aws3
      nc = prod.create_NC_file(name, product, ver, opt1, opt2, opt3, data.ET[0], logfile)
      prod.surface_met(meta, data, nc, ver)
      nc.close() 
         
   del prod

def t_control(logfile): 
   import os
   from collections import namedtuple  
   
   # read in and process config file   
   [ver, dn_in, name, product] = read_config(logfile)
   list = os.listdir(dn_in)
  
   # read in meta file
   meta = read_meta(logfile, name)
   
   #read in data
   data = namedtuple("data", "") 
   data.lat = 51.52028
   data.lon = -0.21333
   
   for fn in list:
      fn_in = os.path.join(dn_in, fn)
      print('Processing file: ',fn)
      data = read_data_file(name, fn_in, data, logfile)
        
      # run through run list for each deployment mode
      do_run(name, product, ver, meta, data, logfile)