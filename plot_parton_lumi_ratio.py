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
parser.add_argument("--denom", type=int, default=0, help="cm energy for denominator (default: skip ratio, plot numer directly)")
parser.add_argument("--yrange", metavar=("ymin","ymax"), type=float, default=(1, 100), nargs=2, help="y axis range")
parser.add_argument("--liny", default=False, action="store_true", help="linear y scale")
parser.add_argument("-v", "--verbose", default=False, action="store_true", help="verbose printouts")
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
    if args.denom>0:
        # including missing 1/s factor
        numer_vals = numer_vals/args.numer**2
        denom_vals = np.asarray(lumis[args.denom][combo])/args.denom**2
        min_length = min(numer_vals.size, denom_vals.size)
        numer_vals = numer_vals[:min_length]
        denom_vals = denom_vals[:min_length]
        mass_vals = masses[:min_length]
        avoid_0 = denom_vals>0
        numer_vals = numer_vals[avoid_0]
        denom_vals = denom_vals[avoid_0]
        mass_vals = mass_vals[avoid_0]
        ratio = numer_vals / denom_vals
        if args.verbose:
            print("mass = {}".format(" ".join("{:g}".format(m) for m in mass_vals)))
            print("{} = {}".format(combo," ".join("{:g}".format(r) for r in ratio)))
    else:
        mass_vals = masses[:numer_vals.size]
        ratio = numer_vals
    ax.plot(mass_vals, ratio, color=colors[ic], linestyle=lines[ic], label=combo_names[ic])

# axes etc.
ax.set_xscale('log')
ax.set_xlim(min(masses), max(masses))
ax.set_xlabel(r"$m_{\mathrm{X}}$ [GeV]")
if not args.liny:
    ax.set_yscale('log')
ax.set_ylim(args.yrange[0],args.yrange[1])
if args.denom>0:
    ax.set_ylabel("luminosity ratio ({:g} TeV / {:g} TeV)".format(args.numer/1000, args.denom/1000))
else:
    ax.set_ylabel("parton luminosity ({:g} TeV) [pb]".format(args.numer/1000, args.denom/1000))
ax.legend()

# save
if args.denom>0:
    fname = "parton_lumi_ratio_{}_{}_{}.pdf".format(args.numer, args.denom, args.pdf)
else:
    fname = "parton_lumi_{}_{}.pdf".format(args.numer, args.pdf)
plt.savefig(fname, bbox_inches='tight')

