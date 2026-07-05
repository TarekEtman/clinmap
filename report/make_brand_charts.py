#!/usr/bin/env python3
"""ClinMAP brand charts: Wilson CIs, discrimination, QA ladder. Cream/ink/rust/teal."""
import json, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from pathlib import Path

CREAM,INK,RUST,TEAL,MUT = '#F7F4EF','#344551','#A95F37','#2E8B8B','#8a95a0'
F = Path('/sessions/pensive-focused-keller/mnt/.claude/skills/canvas-design/canvas-fonts')
try:
    fm.fontManager.addfont(str(F/'CrimsonPro-Regular.ttf')); fm.fontManager.addfont(str(F/'DMMono-Regular.ttf'))
    SERIF, MONO = 'Crimson Pro', 'DM Mono'
except Exception:
    SERIF, MONO = 'serif', 'monospace'
plt.rcParams.update({'figure.facecolor':CREAM,'axes.facecolor':CREAM,'savefig.facecolor':CREAM,
 'axes.edgecolor':MUT,'axes.labelcolor':INK,'xtick.color':INK,'ytick.color':INK,
 'font.family':MONO,'font.size':9,'axes.titlesize':13,'axes.titleweight':'normal',
 'axes.spines.top':False,'axes.spines.right':False,'axes.grid':True,
 'grid.color':INK,'grid.alpha':0.08,'grid.linewidth':0.6})
OUT = Path('report/clinmap_voi_v0_charts'); OUT.mkdir(exist_ok=True)
E = json.load(open('report/benchmark_evidence/clinmap_voi_v0_benchmark_evidence.json'))
M = json.load(open('report/clinmap_voi_v0_performance_metrics.json'))

def short(n): return (n.split('/')[-1])[:24]
def title(ax,t,sub=''):
    ax.set_title(t, fontfamily=SERIF, fontsize=15, color=INK, loc='left', pad=26)
    if sub: ax.text(0,1.015,sub,transform=ax.transAxes,fontsize=7.5,color=MUT)

# 1 — decision accuracy by model (kept filename)
rows=sorted(((short(k),v['decision_accuracy']) for k,v in M['models'].items()),key=lambda r:r[1])
fig,ax=plt.subplots(figsize=(8.6,6.2))
ax.barh([r[0] for r in rows],[r[1] for r in rows],color=INK,height=0.62,alpha=0.88)
ax.barh(rows[-1][0],rows[-1][1],color=TEAL,height=0.62)
ax.axvline(M['aggregate']['mean_decision_accuracy'],color=RUST,lw=1.2,ls='--')
ax.text(M['aggregate']['mean_decision_accuracy'],len(rows)-0.2,' mean',color=RUST,fontsize=8)
ax.set_xlim(0.8,0.96); title(ax,'Decision accuracy by model','ClinMAP-VOI v0 · 3,971 reviewed responses · synthetic probes, not clinical validation')
fig.tight_layout(); fig.savefig(OUT/'decision_accuracy_by_model.svg'); plt.close(fig)

# 2 — metamorphic pass by model (kept filename)
rows=sorted(((short(k),v['metamorphic_pass_rate']) for k,v in M['models'].items()),key=lambda r:r[1])
fig,ax=plt.subplots(figsize=(8.6,6.2))
ax.barh([r[0] for r in rows],[r[1] for r in rows],color=TEAL,height=0.62,alpha=0.9)
ax.axvline(M['aggregate']['mean_metamorphic_pass_rate'],color=RUST,lw=1.2,ls='--')
ax.set_xlim(0.6,0.95); title(ax,'Metamorphic consistency by model','does the answer move when the case quietly changes? · 3,219 relation annotations')
fig.tight_layout(); fig.savefig(OUT/'metamorphic_pass_by_model.svg'); plt.close(fig)

# 3 — Wilson 95% CIs by clinical domain (NEW, proper statistics)
dom=E['gold_stats']['by_domain']
items=sorted(dom.items(),key=lambda kv:kv[1]['gold_match_rate'])
names=[k.replace('_',' ') for k,_ in items]
rate=[v['gold_match_rate'] for _,v in items]
lo=[v['wilson_95_ci'][0] for _,v in items]; hi=[v['wilson_95_ci'][1] for _,v in items]
ns=[v['n'] for _,v in items]
fig,ax=plt.subplots(figsize=(8.6,0.42*len(items)+2))
y=np.arange(len(items))
ax.hlines(y,lo,hi,color=INK,lw=2,alpha=0.55)
ax.plot(rate,y,'o',color=RUST,ms=6,zorder=3)
for i,(r,n) in enumerate(zip(rate,ns)): ax.text(hi[i]+0.008,i,f'n={n}',va='center',fontsize=7,color=MUT)
ax.set_yticks(y,names); ax.set_xlim(min(lo)-0.03,1.005)
title(ax,'Gold-label match rate by clinical domain, Wilson 95% CI','per-domain agreement between framework gold and primary review · point = rate, line = 95% CI')
fig.tight_layout(); fig.savefig(OUT/'wilson_ci_by_domain.svg'); plt.close(fig)

# 4 — accuracy vs metamorphic discrimination scatter (NEW)
fig,ax=plt.subplots(figsize=(8.0,6.4))
xs=[v['decision_accuracy'] for v in M['models'].values()]
ys=[v['metamorphic_pass_rate'] for v in M['models'].values()]
ax.axvline(np.mean(xs),color=MUT,lw=0.8,ls=':'); ax.axhline(np.mean(ys),color=MUT,lw=0.8,ls=':')
ax.scatter(xs,ys,s=54,c=TEAL,edgecolors=INK,linewidths=0.7,zorder=3)
for k,v in M['models'].items():
    ax.annotate(short(k),(v['decision_accuracy'],v['metamorphic_pass_rate']),fontsize=6.4,color=INK,
                xytext=(4,4),textcoords='offset points')
ax.set_xlabel('decision accuracy'); ax.set_ylabel('metamorphic pass rate')
title(ax,'Right answers vs. stable judgment','models above the line keep their reasoning when the case shifts; accuracy alone hides this')
fig.tight_layout(); fig.savefig(OUT/'accuracy_vs_metamorphic.svg'); plt.close(fig)

# 5 — QA ladder (NEW)
a=E['discrimination']['audit_reference']
labels=['full corpus accuracy','holdout accuracy','protocol QC majority','kappa vs blind QC','kappa vs contract pass']
vals=[a['full_decision_accuracy'],a['holdout_decision_accuracy'],a['protocol_qc_majority_agreement_with_primary'],
      a['cohen_kappa_primary_vs_blind_qa'],a['cohen_kappa_primary_vs_contract_pass']]
cols=[INK,INK,INK,RUST,RUST]
fig,ax=plt.subplots(figsize=(8.2,4.4))
ax.barh(labels[::-1],vals[::-1],color=cols[::-1],height=0.56,alpha=0.9)
for i,v in enumerate(vals[::-1]): ax.text(v+0.008,i,f'{v:.3f}',va='center',fontsize=8,color=INK)
ax.axvline(0.74,color=TEAL,lw=1,ls='--'); ax.text(0.741,4.35,'lit. accuracy 0.74',fontsize=7,color=TEAL)
ax.axvline(0.68,color=TEAL,lw=1,ls=':'); ax.text(0.681,-0.55,'lit. kappa 0.68',fontsize=7,color=TEAL)
ax.set_xlim(0.5,1.0)
title(ax,'The reviewer, audited','every number recomputable from the frozen queue · rust = agreement statistics (kappa)')
fig.tight_layout(); fig.savefig(OUT/'qa_ladder.svg'); plt.close(fig)
print('5 charts written to', OUT)
