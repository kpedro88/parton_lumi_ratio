import sys
sys.path.append(".local/lib/python{}.{}/site-packages".format(sys.version_info.major,sys.version_info.minor))
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from parton import PDF, PLumi

parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("--pdf", type=str, default='NNPDF31_nnlo_as_0118_mc_hessian_pdfas', help="PDF name")
parser.add_argument("--pdfdir", type=str, default="pdfs", help="PDF directory")
args = parser.parse_args()

pdf = PDF(args.pdf, 0, args.pdfdir)

# mass = sqrt(s-hat) = Q
mmin = 100
mmax = 10000
mstep = 100
masses = list(range(mmin,mmax+mstep,mstep))
cmenergies = [7000, 8000, 13000, 13600, 14000]

# partons
quarks = [1,2,3,4,5]
antiquarks = [-1,-2,-3,-4,-5]
gluons = [21]

# combos
combos = {}
combos["gg"] = []
for g1,g2 in zip(gluons,gluons):
    combos["gg"].append((g1,g2))
combos["qg"] = []
for g1,q2 in zip(gluons,quarks+antiquarks):
    combos["qg"].extend([
        (g1,q2),
        (q2,g1),
    ])
combos["qq"] = []
for q1,q2 in zip(quarks,antiquarks):
    combos["qq"].extend([
        (q1,q2),
        (q2,q1),
    ])

# set up output
lumis = {}
for cme in cmenergies:
    lumis[cme] = {}
    for combo in combos:
        lumis[cme][combo] = []

# loop over quantities
for mass in masses:
    plumi = PLumi(pdf, Q2=mass**2)
    for cme in cmenergies:
        # tau = s-hat/s
        tau = mass**2/cme**2
        if tau>1: continue
        for combo,pairs in combos.items():
            lumi_combo = 0
            for p1,p2 in pairs:
                # parton luminosity at s-hat/s
                lumi_pair = plumi.L(p1, p2, tau)
                lumi_combo += lumi_pair
            lumis[cme][combo].append(lumi_combo)

with open("lumis_{}.py".format(args.pdf),'w') as outfile:
    objs = [("masses", masses), ("lumis", lumis)]
    for oname, obj in objs:
        outfile.write("{} = {}\n".format(oname,repr(obj)))

