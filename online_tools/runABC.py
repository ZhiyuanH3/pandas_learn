#!/bin/python2.7
#SBATCH --partition=all
#SBATCH --time=00:44:00
#SBATCH --nodes=1
#SBATCH --job-name bdts
#SBATCH --output /home/hezhiyua/logs/tvt_for_bdt-%j.out
#SBATCH --error  /home/hezhiyua/logs/tvt_for_bdt-%j.err
#SBATCH --mail-type END
#SBATCH --mail-user zhiyuan.he@desy.de

import os
from   os import system as act


m_lst = [20,30,40,50]
l_lst = [500,1000,2000,5000]

for m_i in m_lst:
    for l_i in l_lst:
        phsp_str = str(m_i) + '_' + str(l_i)

        act('python trnAvalBtstC_4jet.py '+phsp_str)
        #act('python trnAvalBtstC_2jet.py '+phsp_str)
      



