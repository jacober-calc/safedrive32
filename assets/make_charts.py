import os, math, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Arc, FancyArrowPatch, Rectangle
os.makedirs("assets", exist_ok=True)
INK="#1f2933"; GRID="#d9dee3"; BLUE="#2563eb"; ORANGE="#e8702a"; GREEN="#2f9e44"; GREY="#8a949e"; RED="#c92a2a"; PURPLE="#7048e8"
plt.rcParams.update({"font.size":11,"axes.edgecolor":INK,"axes.labelcolor":INK,"xtick.color":INK,"ytick.color":INK,
 "text.color":INK,"axes.spines.top":False,"axes.spines.right":False,"axes.grid":True,"grid.color":GRID,"grid.linewidth":0.8,
 "figure.facecolor":"white","axes.facecolor":"white","svg.fonttype":"path","axes.titleweight":"bold","axes.titlesize":13})
PREVIEW=os.environ.get("PREVIEW")
def save(fig,name):
    fig.savefig(f"assets/{name}.svg",bbox_inches="tight",facecolor="white")
    if PREVIEW: fig.savefig(f"/tmp/sd_{name}.png",bbox_inches="tight",facecolor="white",dpi=70)
    plt.close(fig)
def box(ax,x,y,w,h,c): ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0,rounding_size=.08",fc="white",ec=c,lw=1.8))
g=9.80665; BUS=12.192

# 1 Program map
fig,ax=plt.subplots(figsize=(10.5,3.9)); ax.axis("off"); ax.set_xlim(0,10.6); ax.set_ylim(0,3.75)
ax.text(.1,3.6,"Program Map",fontsize=13,fontweight="bold",va="center")
groups=[("Safety",BLUE,[("G","Braking:\ng-force"),("D","Braking:\ndistance"),("T","Braking:\ntime"),("X","Braking:\nm/s²"),("S","Safe\nstopping"),("K","Kickout")],.1),
        ("Planning",ORANGE,[("B","Buses\nrequired"),("W","Weight\nand load")],8.1)]
for name,c,items,x0 in groups:
    ax.text(x0,3.05,name,fontsize=11,fontweight="bold",color=c)
    for i,(k,t) in enumerate(items):
        box(ax,x0+i*1.25,1.45,1.15,1.35,c)
        ax.text(x0+i*1.25+.575,2.42,f"LBL {k}",ha="center",fontsize=11.5,fontweight="bold",color=c)
        ax.text(x0+i*1.25+.575,1.88,t,ha="center",va="center",fontsize=9.2)
ax.text(.1,.95,"Internal: V (speed prompt, km/h to m/s), Z (braking results display)",fontsize=9.5,color=GREY)
ax.text(.1,.5,"Flag 1 set: the braking programs also display the stopping distance in 40 ft bus lengths (12.192 m)",fontsize=9.5,color=GREY)
save(fig,"program_map")

# 2 Speed-time triangle
v=50/3.6; a=0.25*g; T=v/a; d=v*T/2
fig,ax=plt.subplots(figsize=(9,4.3))
ax.fill([0,0,T],[0,v,0],color=BLUE,alpha=.18); ax.plot([0,T],[v,0],color=BLUE,lw=2.6)
ax.text(T*.28,v*.3,f"Area = distance\nD = V × T ÷ 2 = {d:.2f} m",fontsize=11,color=BLUE,fontweight="bold")
ax.annotate(f"Slope = deceleration\nX = {a:.3f} m/s²  (G = 0.25)",xy=(T*.55,v*.45),xytext=(T*.62,v*.78),fontsize=10.5,color=ORANGE,arrowprops=dict(arrowstyle="->",color=ORANGE))
ax.annotate("",xy=(T,-.9),xytext=(0,-.9),arrowprops=dict(arrowstyle="<->",color=INK,lw=1.2)); ax.text(T/2,-1.6,f"T = V ÷ X = {T:.2f} s",ha="center",fontsize=10.5)
ax.text(.08,v+.35,"V = 50 km/h = 13.89 m/s",fontsize=10.5)
ax.set_xlim(-.2,T+.6); ax.set_ylim(-2.2,v+1.6); ax.set_xlabel("Time (s)"); ax.set_ylabel("Speed (m/s)")
ax.set_title("Braking to a Stop: One Triangle, Four Values",loc="left"); save(fig,"speed_time")

# 3 Stopping distance vs speed
sp=np.linspace(0,100,200); fig,ax=plt.subplots(figsize=(9,4.4))
for G,c,lab in [(0.20,GREEN,"0.20 g, gentle"),(0.25,BLUE,"0.25 g, typical"),(0.29,ORANGE,"0.29 g, top of acceptable")]:
    ax.plot(sp,(sp/3.6)**2/(2*G*g),color=c,lw=2.3,label=lab)
ax.plot(50,d,"o",color=RED,ms=9,zorder=5); ax.annotate(f"50 km/h at 0.25 g:\n{d:.2f} m = {d/BUS:.2f} bus lengths",xy=(50,d),xytext=(18,95),fontsize=10,color=RED,arrowprops=dict(arrowstyle="->",color=RED))
ax.set_xlim(0,100); ax.set_ylim(0,200); ax.set_xlabel("Speed (km/h)"); ax.set_ylabel("Stopping distance (m)")
sec=ax.secondary_yaxis("right",functions=(lambda m:m/BUS,lambda b:b*BUS)); sec.set_ylabel("40 ft bus lengths")
ax.legend(frameon=False,loc="upper left",fontsize=9.5,bbox_to_anchor=(0,.98))
ax.set_title("Stopping Distance Grows with the Square of Speed",loc="left"); save(fig,"stopping_distance")

# 4 Safe stopping distance
speeds=np.arange(30,101,10); R,F=2.5,0.35
re=speeds/3.6*R; br=(speeds/3.6)**2/(2*g*F)
fig,ax=plt.subplots(figsize=(9,4.4)); ax.grid(axis="x",visible=False)
ax.bar(speeds,re,width=6.5,color=GREEN,alpha=.85,label=f"Reaction: V × R  (R = {R} s)")
ax.bar(speeds,br,bottom=re,width=6.5,color=BLUE,alpha=.85,label=f"Braking: V² ÷ 2g(F + S)  (F = {F}, S = 0)")
for s_,t in zip(speeds,re+br): ax.text(s_,t+2,f"{t:.0f}",ha="center",fontsize=9)
ax.set_xticks(speeds); ax.set_xlabel("Speed (km/h)"); ax.set_ylabel("Distance (m)"); ax.set_ylim(0,210)
ax.legend(frameon=False,loc="upper left",fontsize=9.5)
ax.set_title("Safe Stopping Distance with LBL S: Reaction plus Braking",loc="left"); save(fig,"safe_stopping")

# 4b Road conditions
sp=np.linspace(20,100,200); fig,ax=plt.subplots(figsize=(9,4.4))
for f,lab,c in [(0.7,"Dry, F ≈ 0.7",GREEN),(0.4,"Wet, F ≈ 0.4",BLUE),(0.2,"Packed snow, F ≈ 0.2",PURPLE),(0.1,"Ice, F ≈ 0.1",RED)]:
    ax.plot(sp,sp/3.6*2.5+(sp/3.6)**2/(2*g*f),color=c,lw=2.3,label=lab)
for f,c in [(0.7,GREEN),(0.1,RED)]:
    v=50/3.6; t=v*2.5+v*v/(2*g*f); ax.plot(50,t,"o",color=c,ms=8,zorder=5); ax.text(48.5 if f==0.1 else 51.5,t+(-14 if f==0.7 else 10),f"{t:.1f} m at 50 km/h",fontsize=9.5,color=c,ha="right" if f==0.1 else "left")
ax.set_xlim(20,100); ax.set_ylim(0,500); ax.set_xlabel("Speed (km/h)"); ax.set_ylabel("Safe stopping distance (m)")
ax.legend(frameon=False,loc="upper left",fontsize=9.5,title="Road condition (R = 2.5 s, level)",title_fontsize=9.5)
ax.set_title("Road Conditions Change Everything",loc="left"); save(fig,"road_conditions")

# 5 Tail swing diagram
O,A,C=3.4,30,1.0
fig,ax=plt.subplots(figsize=(8.5,5.4)); ax.set_aspect("equal"); ax.axis("off")
ax.set_xlim(-6.5,5.2); ax.set_ylim(-2.6,4.2)
ax.plot([-6.5,5.2],[-C,-C],color=INK,lw=2.5); ax.text(-6.4,-C-.35,"Curb line",ha="left",fontsize=10)
ax.add_patch(Rectangle((-6.0,0),6.0,2.5,fc="#eef1f4",ec=GREY,lw=1.5,ls="--")); ax.text(-3.0,1.25,"Bus at the stop, about to pull out",ha="center",color=GREY,fontsize=10)
th=math.radians(A); piv=(-O,0)
# rotated body about rear axle pivot at x=-O? Use pivot at rear axle (x=0 is rear end before turn? simplify: pivot at origin-left)
px,py=0,0; rear=(px+O*math.cos(math.pi+th)*-1,0)
end=(O*math.cos(th),-O*math.sin(th))
ax.plot([0,O],[0,0],color=GREY,lw=1.5,ls="--"); ax.plot([0,end[0]],[0,end[1]],color=ORANGE,lw=4)
ax.plot(0,0,"o",color=INK,ms=8); ax.text(-.15,.3,"Rear axle",ha="right",fontsize=10)
ax.text(O/2,.25,f"Rear overhang O = {O} m",fontsize=10,color=ORANGE,ha="center")
ax.add_patch(Arc((0,0),2.2,2.2,theta1=-A,theta2=0,color=PURPLE,lw=1.6)); ax.text(1.2,-.35,f"A = {A}°",fontsize=10,color=PURPLE)
ax.plot([end[0],end[0]],[0,end[1]],color=RED,lw=1.6,ls=":")
ax.annotate("",xy=(end[0]+.35,end[1]),xytext=(end[0]+.35,0),arrowprops=dict(arrowstyle="<->",color=RED,lw=1.4))
ax.text(end[0]+.55,end[1]/2+.25,f"O·sin A\n= {O*math.sin(th):.2f} m",fontsize=10,color=RED,va="center")
ax.annotate("",xy=(-1.3,-C),xytext=(-1.3,0),arrowprops=dict(arrowstyle="<->",color=GREEN,lw=1.4)); ax.text(-1.45,-C/2,f"C = {C} m",fontsize=10,color=GREEN,ha="right",va="center")
ax.text(-6.4,-2.2,f"Kickout = O·sin A − C = {O*math.sin(th)-C:.2f} m past the curb line (positive = the rear kicks out over the curb)",fontsize=10.5,fontweight="bold",color=RED)
ax.text(-6.4,4.0,"Kickout on Departure with LBL K",fontsize=13,fontweight="bold",va="center")
ax.text(-6.4,3.45,f"Steering away from the curb through angle A swings the rear overhang toward it",fontsize=10,color=GREY,va="center")
save(fig,"kickout")

# 6 Load along a route
W=6500; on=[12,10,9,9,25,5,3,2,1,0]; off=[0,0,0,0,0,12,12,14,14,10]
N=[]; n=0
for i,(a_,o_) in enumerate(zip(on,off)): n=n+a_-o_; N.append(n)
stops=np.arange(1,len(N)+1); pct=np.array(N)*86/W*100
fig,ax=plt.subplots(figsize=(9.5,4.4)); ax.grid(axis="x",visible=False)
cols=[ORANGE if i==4 else BLUE for i in range(len(N))]
ax.bar(stops,pct,color=cols,alpha=.88,width=.7)
for x_,p_,n_ in zip(stops,pct,N): ax.text(x_,p_+1.5,f"{n_}",ha="center",fontsize=9)
ax.axhline(100,color=RED,ls="--",lw=1.3); ax.text(.6,102,f"Weight limit W = {W:,} kg",fontsize=10,color=RED)
ax.annotate("Stop 5: 25 board\n40 → 65 passengers\n3,440 → 5,590 kg\n52.9% → 86.0%",xy=(5,86),xytext=(7.7,72),fontsize=10,color=ORANGE,fontweight="bold",arrowprops=dict(arrowstyle="->",color=ORANGE))
ax.set_xticks(stops); ax.set_xlabel("Stop"); ax.set_ylabel("Load, % of W (86 kg per passenger)"); ax.set_ylim(0,112); ax.set_xlim(.4,10.6)
ax.set_title("Weight and Load with LBL W: one stop can add 2,150 kg",loc="left"); save(fig,"route_load")

# 7 Buses required
H=np.arange(5,31); cyc=70; need=cyc/H
fig,ax=plt.subplots(figsize=(9,4.2))
ax.plot(H,need,color=GREY,lw=1.5,ls="--",label="(P + L) ÷ H")
ax.step(H,np.ceil(need-1e-9),where="mid",color=BLUE,lw=2.4,label="Buses to schedule (rounded up)")
ax.plot(15,cyc/15,"o",color=ORANGE,ms=9,zorder=5); ax.annotate("H = 15 min: 4.67 → 5 buses",xy=(15,cyc/15),xytext=(17,8.5),fontsize=10,color=ORANGE,arrowprops=dict(arrowstyle="->",color=ORANGE))
ax.plot(17.5,4,"s",color=RED,ms=9,zorder=5); ax.annotate("Only 4 buses: H = 70 ÷ 4 = 17.5 min,\n1.17 × the passengers per bus",xy=(17.5,4),xytext=(19,6),fontsize=10,color=RED,arrowprops=dict(arrowstyle="->",color=RED))
ax.set_xlim(5,30); ax.set_ylim(0,15); ax.set_xlabel("Headway H (minutes)"); ax.set_ylabel("Buses")
ax.legend(frameon=False,loc="upper right",fontsize=9.5)
ax.set_title("Buses Required with LBL B (paddle 60 min + layover 10 min)",loc="left"); save(fig,"buses_required")
