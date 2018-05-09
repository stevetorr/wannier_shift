import sys
import numpy as np
from multiprocessing import Pool
import time

# this script is the wrapper script to reprocess (post-process) on the raw VASP+Wannier90 simulation data

def proc_wan_oneset(inds):

    # read in the configuration file to extract relevant information
    pos_file='allpos/POSCAR_'+str(inds)
    fname_wan='data/biTaS2_'+str(inds)+'_hr.dat'
    # will write the results to this file
    fname_convert='data/new_proc_wan_'+str(inds)


    # this section starts to read in the information and reprocess them into the information to be written into the postprocess file
    fidpos=open(pos_file,'r')
    linehead=fidpos.readline().strip()
    scale_fac=float(fidpos.readline().strip())

    # reconstruct the primitive lattice vectors
    a1_vec=fidpos.readline().strip()
    a2_vec=fidpos.readline().strip()
    a3_vec=fidpos.readline().strip()
 
    a1_vec=scale_fac*np.asarray(list(map(float,a1_vec.split())))
    a2_vec=scale_fac*np.asarray(list(map(float,a2_vec.split())))
    a3_vec=scale_fac*np.asarray(list(map(float,a3_vec.split())))

    # read the atomic types and their numbers
    atom_types=fidpos.readline().strip().split()
    atom_types_num=list(map(int,fidpos.readline().strip().split()))
    atom_totnum=(np.sum(atom_types_num))

    # cartesian or direct coordination, not relevant here, always cartesian
    fidpos.readline()  

    # read basis atom position
    all_atom_pos=[]
    for inda in range(0,atom_totnum):
        tmppos=list(map(float,fidpos.readline().strip().split()))
        all_atom_pos.append(np.asarray(tmppos))

    fidpos.close()

    # these are the orbital types
    d_orb=['dz2','dxz','dyz','dx2y2','dxy']
    p_orb=['pz','px','py']

    wan_orbs=d_orb+d_orb+p_orb+p_orb+p_orb+p_orb

    wan_atom=[]
    for inda in range(0,10):
        wan_atom.append(atom_types[0])
    for inda in range(0,12):
        wan_atom.append(atom_types[1])

    wan_pos=[]
    for inda in range(0,5):
        wan_pos.append(all_atom_pos[0])
    for inda in range(0,5):
        wan_pos.append(all_atom_pos[1])
    for inda in range(0,3):
        wan_pos.append(all_atom_pos[2])
    for inda in range(0,3):
        wan_pos.append(all_atom_pos[3])
    for inda in range(0,3):
        wan_pos.append(all_atom_pos[4])
    for inda in range(0,3):
        wan_pos.append(all_atom_pos[5])

    fid=open(fname_wan,'r')
    linehead=fid.readline().strip()

    num_wann=int(fid.readline().strip())
    num_Rs=int(fid.readline().strip())

    # degeneracy factors from the conventions in Wannier90 code
    element_per_line = 15
    tmp_full=num_Rs // element_per_line
    tmp_extra=num_Rs-tmp_full*element_per_line

    degen_fac=[]

    for indl in range(0,tmp_full):
        tmpstr=fid.readline().strip().split()
        degen_fac=degen_fac+tmpstr

    if tmp_extra>0:
        tmpstr=fid.readline().strip().split()
        degen_fac=degen_fac+tmpstr

    degen_fac=list(map(float,degen_fac))


    output_str=[]
    # strain field for future generalization
    strain_uxxyy=0.0
    strain_uxxmyy=0.0
    strain_uxy=0.0
    layer_h=all_atom_pos[1][2]-all_atom_pos[0][2]
    output_head='atom_from_type,atom_from_orbital,atom_from_index,atom_to_type,atom_to_orbital,atom_to_index'
    output_head=output_head+',hop_vec_x,hop_vec_y,hop_vec_z,ham_real,ham_imag'
    output_head=output_head+',a1_x,a1_y,a2_x,a2_y,layer_h'

    # with the information extracted above, we will write them into the postprocess file with the header for each column.
    fid_convert=open(fname_convert,'w')
    fid_convert.write(output_head+'\n')

    for indR in range(0,num_Rs):
        tmp_degen=degen_fac[indR]
        tmp_output=[]
        for indh in range(0,num_wann*num_wann):
            tmp_str=''
            tmp_read=fid.readline().strip().split()
            n1=int(tmp_read[0])
            n2=int(tmp_read[1])
            n3=int(tmp_read[2])
            orb1=int(tmp_read[3])
            orb2=int(tmp_read[4])
            ham_real=float(tmp_read[5])/tmp_degen
            ham_imag=float(tmp_read[6])/tmp_degen

            tmp_vec=-(a1_vec*float(n1)+a2_vec*float(n2)+a3_vec*float(n3))

            to_pos=wan_pos[orb1-1]
            from_pos=wan_pos[orb2-1]
            to_orb=wan_orbs[orb1-1]
            from_orb=wan_orbs[orb2-1]
            to_atom=wan_atom[orb1-1]
            from_atom=wan_atom[orb2-1]

            hop_vec=to_pos+tmp_vec-from_pos

            tmp_str=from_atom+','+from_orb+','+str(orb2)+','+to_atom+','+to_orb+','+str(orb1)
            tmp_str=tmp_str+','+str(hop_vec[0])+','+str(hop_vec[1])+','+str(hop_vec[2])
            tmp_str=tmp_str+','+str(ham_real)+','+str(ham_imag)
            tmp_str=tmp_str+','+str(a1_vec[0])+','+str(a1_vec[1])+','+str(a2_vec[0])+','+str(a2_vec[1])+','+str(layer_h)
            tmp_output.append(tmp_str)

        for outputline in tmp_output:
            fid_convert.write(outputline+'\n')

    fid.close()
    fid_convert.close()



if __name__== "__main__":

    all_parms=range(0,400)
    npp=1
    pool = Pool(npp)
    tstart=time.time()
    pool.map(proc_wan_oneset,all_parms)
    tend=time.time()

    print('Elapsed time: ' +str(tend-tstart)+'s with Num_process='+str(npp))




