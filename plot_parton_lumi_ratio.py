import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

def import_attrs(pyname, attrs):
    if not isinstance(attrs,list):
        attrs = [attrs]
    tmp = __import__(pyname.replace(".py","").replace("/","."), fromlist=attrs)
    if len(attrs)==1:
        return getattr(tmp,attrs[0])
    else:
        return [getattr(tmp,attr) for attr in attrs]

parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("--pdf", type=str, default='NNPDF31_nnlo_as_0118_mc_hessian_pdfas', help="PDF name")
parser.add_argument("--numer", type=int, required=True, help="cm energy for numerator")
parser.add_argument("--denom", type=int, required=True, help="cm energy for denominator")
parser.add_argument("--yrange", metavar=("ymin","ymax"), type=float, default=(1, 100), nargs=2, help="y axis range (None=auto)")
args = parser.parse_args()

masses, lumis = import_attrs("lumis_{}.py".format(args.pdf), ["masses", "lumis"])

# style etc.
plt.rcParams.update({'font.size': 20})
combos = ["gg","qq","qg"]
combo_names = [r"gg", r"$\Sigma q\overline{q}$", "qg"]
colors = ["#5790fc", "#e42536", "#964a8b"]
lines = ["solid", "dashed", "dashdot"]

# calculate & plot ratios
masses = np.asarray(masses)
fig, ax = plt.subplots(figsize=(9, 7))
for ic,combo in enumerate(combos):
    numer_vals = np.asarray(lumis[args.numer][combo])
    denom_vals = np.asarray(lumis[args.denom][combo])
    min_length = min(numer_vals.size, denom_vals.size)
    numer_vals = numer_vals[:min_length]
    denom_vals = denom_vals[:min_length]
    mass_vals = masses[:min_length]
    avoid_0 = denom_vals>0
    numer_vals = numer_vals[avoid_0]
    denom_vals = denom_vals[avoid_0]
    mass_vals = mass_vals[avoid_0]
    ratio = numer_vals / denom_vals
    ax.plot(mass_vals, ratio, color=colors[ic], linestyle=lines[ic], label=combo_names[ic])

# axes etc.
ax.set_xscale('log')
ax.set_xlim(min(masses), max(masses))
ax.set_xlabel(r"$m_{\mathrm{X}}$ [GeV]")
ax.set_yscale('log')
ax.set_ylim(args.yrange[0],args.yrange[1])
ax.set_ylabel("luminosity ratio ({:g} TeV / {:g} TeV)".format(args.numer/1000, args.denom/1000))
ax.legend()

# save
fname = "parton_lumi_ratio_{}_{}_{}.pdf".format(args.numer, args.denom, args.pdf)
plt.savefig(fname, bbox_inches='tight')

