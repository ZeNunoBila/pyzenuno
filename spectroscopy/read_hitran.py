# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 19:32:45 2021

from pytran

@author: justin.erwin@aeronomie.be & severine.robert@aeronomie.be
"""

def build_line(M, I, vc, S, Acoeff, gamma_foreign, gamma_self, Epp, N, delta, 
               Vp, Vpp, Qp, Qpp, Ierr_vc, Ierr_S, Ierr_gforeign, Ierr_gself, 
               Ierr_N, Ierr_delta, Iref_vc, Iref_S, Iref_gforeign, Iref_gself, 
               Iref_N, Iref_delta, flag, gp, gpp):
    
    g_foreign_str = '%5.4f' %gamma_foreign
    g_foreign_str = g_foreign_str.lstrip('0')
    
    gself_str = '%5.3f'%gamma_self
    
    shift_str = '%8.6f'%abs(delta)
    if delta < 0:
        shift_str = shift_str.lstrip('0')
        shift_str = '-' + shift_str
    
    N_str = '%4.2f'%abs(N)
    if N < 0:
        N_str = N_str.lstrip('0')
        N_str = '-' + N_str
    
    line_p0 = '%2s%1s%12.6f%10.3E%10.3E' %(M, I, vc, S, Acoeff)
    line_p1 = '%5s%5s%10.4f%4s%8s' %(g_foreign_str, gself_str, Epp, N_str, shift_str)
    line_p2 = '%15s%15s%15s%15s' %(Vp, Vpp, Qp, Qpp)
    line_p3 = '%1s%1s%1s%1s%1s%1s'%(Ierr_vc, Ierr_S, Ierr_gforeign, Ierr_gself, Ierr_N, Ierr_delta)
    line_p4 = '%2s%2s%2s%2s%2s%2s'%(Iref_vc, Iref_S, Iref_gforeign, Iref_gself, Iref_N, Iref_delta)
    line_p5 = '%1s%1s%1s'%(flag, gp, gpp)
       
    new_line = line_p0 + line_p1 + line_p2 + line_p3 + line_p4 + line_p5
    return new_line



def read_hitran_parfile(filename, wavemin=0., wavemax=60000., Smin=0.):
    """
    Given a HITRAN2012-format text file, read in the parameters of the molecular absorption features.

    Parameters
    ----------
    filename : str
        The filename to read in.

    Return
    ------
    linelist : dict
        The dictionary of HITRAN linelist for the molecule.
    """
    import numpy as np

    if filename.endswith('.zip'):
        import zipfile
        import os
        zipf = zipfile.ZipFile(filename, 'r')
        (object_name, ext) = os.path.splitext(os.path.basename(filename))
        print(object_name, ext)
        filehandle = zipf.read(object_name).splitlines()
    else:
        filehandle = open(filename, 'r')

    linelist = {
                'M':[],               ## molecule identification number
                'I':[],               ## isotope number
                'vc':[],              ## line center wavenumber (in cm^{-1})
                'S':[],               ## line strength, in cm^{-1} / (molecule cm^{-2})
                'Acoeff':[],          ## Einstein A coefficient (in s^{-1})
                'gamma_foreign':[],       ## line HWHM for air-broadening
                'gamma_self':[],      ## line HWHM for self-emission-broadening
                'Epp':[],             ## energy of lower transition level (in cm^{-1})
                'N':[],               ## temperature-dependent exponent for "gamma-air"
                'delta':[],           ## air-pressure shift, in cm^{-1} / atm
                'Vp':[],              ## upper-state "global" quanta index
                'Vpp':[],             ## lower-state "global" quanta index
                'Qp':[],              ## upper-state "local" quanta index
                'Qpp':[],             ## lower-state "local" quanta index
                'Ierr_vc':[], 
                'Ierr_S':[],
                'Ierr_gforeign':[],
                'Ierr_gself':[], 
                'Ierr_N':[], 
                'Ierr_delta':[],
                'Iref_vc':[], 
                'Iref_S':[], 
                'Iref_gforeign':[], 
                'Iref_gself':[], 
                'Iref_N':[], 
                'Iref_delta':[],                
                'Ierr':[],            ## uncertainty indices
                'Iref':[],            ## reference indices
                'flag':[],            ## flag
                'gp':[],              ## statistical weight of the upper state
                'gpp':[],             ## statistical weight of the lower state
                'comments':[]
                }

    print('Reading "' + filename + '" ...')

    for line in filehandle:

        if (line[0] == '#'):
            continue

        if (len(line) < 160):
            raise ImportError('The imported file ("' + filename + '") does not appear to be a HITRAN2012-format data file.')

        vc = np.float64(line[3:15])
        S = np.float64(line[15:25])
        if vc > wavemax:
            break  # don't need to continue to save
        if ((wavemin <= vc) and (S > Smin)):
            linelist['M'].append(np.uint(line[0:2]))
            #I = line[2]
            # if I == '0':
            #     linelist['I'].append(np.uint(10))
            # elif I == 'A':
            #     linelist['I'].append(np.uint(11))
            # elif I == 'B':
            #     linelist['I'].append(np.uint(11))
            # else:
            #    linelist['I'].append(np.uint(line[2]))
            linelist['I'].append(line[2])
            linelist['vc'].append(np.float64(line[3:15]))
            linelist['S'].append(np.float64(line[15:25]))
            linelist['Acoeff'].append(np.float64(line[25:35]))
            linelist['gamma_foreign'].append(np.float64(line[35:40]))
            linelist['gamma_self'].append(np.float64(line[40:45]))
            linelist['Epp'].append(np.float64(line[45:55]))
            linelist['N'].append(np.float64(line[55:59]))
            linelist['delta'].append(np.float64(line[59:67]))
            linelist['Vp'].append(line[67:82])
            linelist['Vpp'].append(line[82:97])
            linelist['Qp'].append(line[97:112])
            linelist['Qpp'].append(line[112:127])
            linelist['Ierr_vc'].append(line[127:128])
            linelist['Ierr_S'].append(line[128:129])
            linelist['Ierr_gforeign'].append(line[129:130])
            linelist['Ierr_gself'].append(line[130:131])
            linelist['Ierr_N'].append(line[131:132])
            linelist['Ierr_delta'].append(line[132:133])            
            linelist['Iref_vc'].append(line[133:135])
            linelist['Iref_S'].append(line[135:137])
            linelist['Iref_gforeign'].append(line[137:139])
            linelist['Iref_gself'].append(line[139:141])
            linelist['Iref_N'].append(line[141:143])
            linelist['Iref_delta'].append(line[143:145])
            linelist['flag'].append(line[145])
            linelist['gp'].append(line[146:153])
            linelist['gpp'].append(line[153:160])
            linelist['comments'].append(line[160:])

    if filename.endswith('.zip'):
        zipf.close()
    else:
        filehandle.close()

    for key in linelist:
        linelist[key] = np.array(linelist[key])

    return linelist