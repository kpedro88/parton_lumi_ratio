# Parton luminosity ratios

## Setup

```
HOME=$PWD python3 -m pip install parton --user
mkdir pdfs
export PYTHON3PATH=$(python3 -c 'import sys; print(".local/lib/python{}.{}/site-packages".format(sys.version_info.major,sys.version_info.minor))'):$PYTHON3PATH
python3 -m parton --listdir pdfs update
python3 -m parton --listdir pdfs --pdfdir pdfs install [pdfname]
```
substituting the actual PDF name for `[pdfname]` in the last command and repeating for any PDFs needed.

## Usage

Calculation:
```
python3 calc_parton_lumi.py --pdf MSTW2008nlo68cl
```

Plotting:
```
python3 plot_parton_lumi_ratio.py --pdf MSTW2008nlo68cl --numer 13000 --denom 8000
python3 plot_parton_lumi_ratio.py --pdf MSTW2008nlo68cl --numer 13600 --denom 13000 --yrange 1 10
```

## Credits

The calculation uses [parton](https://github.com/DavidMStraub/parton) and [LHAPDF](https://lhapdf.hepforge.org/).

The plotting uses numpy and matplotlib.
