import os
import sys
import shutil
import time

# this script is to carry out the VASP/DFT+Wannier90 simulations for all 400 configurations. This should be called from the job submission file.

main_dir=os.getcwd()+'/'
#tmp_dir=main_dir+'temp/'

# loop over all 400 configurations
for indk in range(0,400):

    # copy the KSCAN folder as the backbone to start with VASP+Wannier simulation
    kdir='KSCAN_'+str(indk)
    os.system('cp -r KSCAN '+kdir)

    # copy the specific files for each configuration
    os.chdir(main_dir+kdir)   
    shutil.copyfile('../allpos/POSCAR_'+str(indk),main_dir+kdir+'/SCF/POSCAR')
    shutil.copyfile('../allpos/POSCAR_'+str(indk),main_dir+kdir+'/WAN/POSCAR')
    shutil.copyfile('../allpos/POSCAR_'+str(indk),main_dir+kdir+'/BANDS/POSCAR')
    shutil.copyfile('../allpos/wannier90_'+str(indk),main_dir+kdir+'/WAN/wannier90.win')

    # self-consistent VASP DFT run
    os.chdir(main_dir+kdir+'/SCF')
    os.system('mpirun -np 8  vasp.5.4.4.w90-1.2.std')
    os.system('cp CHG* ../WAN')
    os.system('cp CHG* ../BANDS')
    os.system('cp LOCPOT ../../data/LOCPOT_'+str(indk))
    os.system('rm WAVE*')

    # non self-consistent band structure run
    os.chdir(main_dir+kdir+'/BANDS')
    os.system('mpirun -np 8  vasp.5.4.4.w90-1.2.std')
    os.system('cp EIGENVAL ../../data/EIGENVAL_'+str(indk))
    os.system('rm WAVE* CHG*')

    # non self-consistent DFT VASP+Wannier90 run
    os.chdir(main_dir+kdir+'/WAN')
    # first the vasp execution
    os.system('mpirun -np 8  vasp.5.4.4.w90-1.2.std')
    # wannier90 simulation
    os.system('wannier90.2.0.1.x wannier90')
    # copy the simulation results essential files to the data folder
    os.system('cp *.win ../../data/biTaS2_'+str(indk)+'.win')
    os.system('cp *.dat ../../data/biTaS2_'+str(indk)+'_hr.dat')
    os.system('cp *.xyz ../../data/biTaS2_'+str(indk)+'_centres.xyz')
    os.system('cp *.r2mn ../../data/biTaS2_'+str(indk)+'.r2mn')
    os.system('rm WAVE* CHG* *.mmn *.amn *.chk')

    # reset the folder
    os.chdir(main_dir)



