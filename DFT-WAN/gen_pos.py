import numpy as np

# this script generates the configurations for the crystal to be sampled (TaS2 bilayer with shifts)

if __name__ == "__main__":

    # prepare the a1 a2 primitive vectors for the crystal in units of A.
    aavec=np.array([ 2.8700000000000001, -1.6570000000000000])
    aalen=np.sqrt(np.dot(aavec,aavec))
    a1=aalen*np.array([ np.sqrt(3)*0.5,-0.5,0.0])
    a2=aalen*np.array([ np.sqrt(3)*0.5,0.5,0.0])

    # define the sampling of the mesh for the shifts
    numscan1=20
    numscan2=20

    indkk=0

    allpos0=[]
    # crystal parameter for the TaS2 (layer height and atomic distance between X atom and M atom plane)
    layer_h=6.0485
    MX_dist=1.567032578994322

    # setup the basis atom positions before shifts applied
    allpos0.append(np.array([0.0,0.0,0.0]))
    allpos0.append(np.array([0.0,0.0,layer_h]))
    tmpvec=(a1+a2)/3.0
    allpos0.append(tmpvec+np.array([0.0,0.0,MX_dist]))
    allpos0.append(tmpvec+np.array([0.0,0.0,-MX_dist]))
    allpos0.append(tmpvec+np.array([0.0,0.0,layer_h+MX_dist]))
    allpos0.append(tmpvec+np.array([0.0,0.0,layer_h-MX_dist]))

    # double check the initial configuration
    print(allpos0)

    # loop over the shifts sampling
    for ind1 in range(0,numscan1):
        for ind2 in range(0,numscan2):
            tmpvec=a1*float(ind1)/numscan1+a2*float(ind2)/numscan2

            # new basis positions after shift applied from sampling
            allpostmp=np.copy(allpos0)
            allpostmp[1][0]=allpostmp[1][0]+tmpvec[0]
            allpostmp[4][0]=allpostmp[4][0]+tmpvec[0]
            allpostmp[5][0]=allpostmp[5][0]+tmpvec[0]
            allpostmp[1][1]=allpostmp[1][1]+tmpvec[1]
            allpostmp[4][1]=allpostmp[4][1]+tmpvec[1]
            allpostmp[5][1]=allpostmp[5][1]+tmpvec[1]

            # writes the crystal structure information to the POSCAR file for running VASP DFT
            fid1=open('allpos/POSCAR_'+str(indkk),"w") 

            fid1.write('TaS2  bilayer sheet \n')
            fid1.write('   1.00000000000000  \n')
            fid1.write('   '+str(a1[0])+'    '+str(a1[1])+'   0.0\n')
            fid1.write('   '+str(a2[0])+'    '+str(a2[1])+'   0.0\n')
            fid1.write('     0.0000000000000000    0.0000000000000000   22 \n')
            fid1.write('   Ta   S  \n')
            fid1.write('   2   4 \n')
            fid1.write('Cartesian \n')

            for inda in range(0,6):
                tmpatom=allpostmp[inda]
                fid1.write('  '+str(tmpatom[0])+'  '+str(tmpatom[1])+'  '+str(tmpatom[2])+'\n')
 
            fid1.close()

            # writes the input parameters and configurations files for running Wannier90 with this sample geometry
            fid2=open('allpos/wannier90_'+str(indkk),"w")
            fid2.write( 'write_xyz = true \n' )
            fid2.write( 'hr_plot = true \n' )
            fid2.write( 'num_dump_cycles = 10 \n' )
            fid2.write( 'write_r2mn = true \n' )
            fid2.write( 'iprint = 2 \n' )
            fid2.write( 'length_unit = Ang \n' )
            fid2.write( 'num_bands = 32 \n' )
            fid2.write( 'dis_num_iter = 20000 \n' )
            fid2.write( 'num_print_cycles = 10 \n' )
            fid2.write( 'num_wann = 22 \n' )
            fid2.write( 'num_iter = 100 \n' )
            fid2.write( 'dis_froz_min = -9.0 \n' )
            fid2.write( 'dis_froz_max = 3.8 \n' )
            fid2.write( 'dis_win_min = -10 \n' )
            fid2.write( 'dis_win_max = 6.9 \n' )
            fid2.write( 'search_shells = 400 \n' )
            fid2.write( 'kmesh_tol = 0.0000000001 \n' )
            fid2.write( '\n\n\n' )

            fid2.write('begin projections \n')
            fid2.write(' Ang \n')

            for inda in range(0,2):
                tmpatom=allpostmp[inda]
                fid2.write(' c='+str(tmpatom[0])+','+str(tmpatom[1])+','+str(tmpatom[2])+': l=2\n')

            for inda in range(2,6):
                tmpatom=allpostmp[inda]
                fid2.write(' c='+str(tmpatom[0])+','+str(tmpatom[1])+','+str(tmpatom[2])+': l=1\n')


            fid2.write('end projections \n')
            fid2.close()


            indkk=indkk+1




