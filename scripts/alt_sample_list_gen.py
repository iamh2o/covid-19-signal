import os
import sys

### Util script to take our fqgz files and make marigold sample sheets.

fq_path = sys.argv[1].rstrip('/')
if fq_path.startswith('/'):
    pass
else:
    raise Exception("ERROR- argument 1 must be an absolute path to the fastq.gz dir starting with '/'\n\n")

out_samp_sheet = sys.argv[2]
w = open(out_samp_sheet,'w')

samp_fqs = {}

fqs = os.popen(f"ls -1 {fq_path}/*fastq.gz")

for i in fqs.readlines():
    f = i.rstrip()
    sl = f.split('/')
    ru = sl[6]
    ex = sl[5]
    samps = f.split('/')[-1].split('.')[0]
    ssl = samps.split('_')
    lane = ssl[2].replace('0','').replace('L','')
    sq = ssl[0]
    r = ssl[3]
    samp = f"{ru}_{ex}_{sq}_{lane}"
    #from IPython import embed
    #embed()
    #raise
    if samp in samp_fqs:
        samp_fqs[samp][r] = f
    else:
        samp_fqs[samp] = {'lane': lane, 'ru': ru, 'ex':ex,'sq':sq, r:f}

w.write("sample,r1_path,r2_path\n")
for i in samp_fqs:
    try:
        print(i,samp_fqs[i]['R1'],samp_fqs[i]['R2'])
    except Exception as e:
        print(f'THIS failed to print!!!! {i} ... {samp_fqs[i]}',e)

    try:
        w.write(f"{i},{samp_fqs[i]['R1']},{samp_fqs[i]['R2']}\n")
    except Exception as e:
        print(f'THIS failed to write!!!! {i} ... {samp_fqs[i]}',e)
w.close()

print(f"\n\n\t\t Your sample sheet is ready: {out_samp_sheet}\n\n")
