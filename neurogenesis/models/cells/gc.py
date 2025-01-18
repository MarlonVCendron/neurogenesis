from brian2 import *

N_granule = 1

# # Synaptic current equations @ SOMA
# eq_soma = Equations('''
# I_syn_g = I_nmda_eg + I_ampa_eg + I_nmda_mg + I_ampa_mg + I_nmda_gn + I_ampa_gn + I_gaba_bg +I_gaba_hg + I_Sahp : amp
# I_nmda_eg = g_nmda_eg*(vm - E_nmda)*s_nmda_eg/(1.0 + eta*Mg*exp(-gamma*vm))                                     : amp
# I_ampa_eg = g_ampa_eg*(vm - E_ampa)*s_ampa_eg                                                                   : amp
# s_nmda_eg                                                                                                       : 1
# s_ampa_eg                                                                                                       : 1
# I_nmda_mg = g_nmda_mg*(vm - E_nmda)*s_nmda_mg/(1.0 + eta*Mg*exp(-gamma*vm))                                     : amp
# I_ampa_mg = g_ampa_mg*(vm - E_ampa)*s_ampa_mg                                                                   : amp
# s_nmda_mg                                                                                                       : 1
# s_ampa_mg                                                                                                       : 1
# I_gaba_bg = g_gaba_bg*(vm - E_gaba)*s_gaba_bg                                                                   : amp
# s_gaba_bg                                                                                                       : 1
# I_gaba_hg = g_gaba_hg*(vm - E_gaba)*s_gaba_hg                                                                   : amp
# s_gaba_hg                                                                                                       : 1
# I_nmda_gn = g_nmda_gn*(vm - E_nmda)*s_nmda_gn*(1.0 + eta*Mg*exp(-gamma*vm))                                     : amp
# I_ampa_gn = g_ampa_gn*(vm - E_ampa)*s_ampa_gn                                                                   : amp
# s_nmda_gn                                                                                                       : 1
# s_ampa_gn                                                                                                       : 1
# I_Sahp                                                                                                          : amp
# dI_Sahp/dt = (g_ahp*(vm-El_g)-I_Sahp)/tau_ahp                                                                   : amp
# ''')


# Tentando fazer igual o artigo
# eq_g = Equations('''
# I_syn_g = I_nmda_eg + I_ampa_eg + I_nmda_mg + I_ampa_mg + I_nmda_gn + I_ampa_gn + I_gaba_bg +I_gaba_hg + I_Sahp : amp
# I_nmda_eg = g_nmda_eg*(vm - E_nmda)*s_nmda_eg/(1.0 + eta*Mg*exp(-gamma*vm))                                     : amp
# I_ampa_eg = g_ampa_eg*(vm - E_ampa)*s_ampa_eg                                                                   : amp
# s_nmda_eg                                                                                                       : 1
# s_ampa_eg                                                                                                       : 1
# I_nmda_mg = g_nmda_mg*(vm - E_nmda)*s_nmda_mg/(1.0 + eta*Mg*exp(-gamma*vm))                                     : amp
# I_ampa_mg = g_ampa_mg*(vm - E_ampa)*s_ampa_mg                                                                   : amp
# s_nmda_mg                                                                                                       : 1
# s_ampa_mg                                                                                                       : 1
# I_gaba_bg = g_gaba_bg*(vm - E_gaba)*s_gaba_bg                                                                   : amp
# s_gaba_bg                                                                                                       : 1
# I_gaba_hg = g_gaba_hg*(vm - E_gaba)*s_gaba_hg                                                                   : amp
# s_gaba_hg                                                                                                       : 1
# I_nmda_gn = g_nmda_gn*(vm - E_nmda)*s_nmda_gn*(1.0 + eta*Mg*exp(-gamma*vm))                                     : amp
# I_ampa_gn = g_ampa_gn*(vm - E_ampa)*s_ampa_gn                                                                   : amp
# s_nmda_gn                                                                                                       : 1
# s_ampa_gn                                                                                                       : 1
# I_Sahp                                                                                                          : amp
# dI_Sahp/dt = (g_ahp*(vm-El_g)-I_Sahp)/tau_ahp                                                                   : amp
# ''')

# dvm/dt = (I_leak + I_K + I_Na + I_inj)/C : volt
MembraneEquation = '''
dvm/dt = (I_L + I_AHP + I_syn)/C : volt
I_L = g_L * (vm - V_L)           : amp
'''

Cm_g      =   0.08   * nF  # membrane capacitance
C         =   0.08   * nF  # membrane capacitance

granule_eqs = MembraneEquation
# granule_eqs += leak_current(gl_g, El_g)
# granule_eqs += IonicCurrent('I = I_syn_g : amp')
# granule_eqs = eq_g


# granule = NeuronGroup(N_granule, model=granule_eqs, threshold='vm > v_th_g',
#                       reset='vm = v_reset_g; I_Sahp += 0.0450*nA',
#                       refractory=20 * ms, compile=True, freeze=True)
granule = NeuronGroup(N_granule, model=granule_eqs, threshold='vm > v_th_g',
                      reset='vm = v_reset_g',
                      refractory=20 * ms)
