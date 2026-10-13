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
groups=[("Braking: enter speed and any one value",BLUE,[("G","g-force"),("D","Distance"),("T","Time"),("X","m/s²")],.1),
        ("Sight",GREEN,[("S","Stopping\nsight")],5.6),("Bus planning",ORANGE,[("K","Tail swing"),("W","Load"),("B","Buses")],7.0)]
for name,c,items,x0 in groups:
    ax.text(x0,3.05,name,fontsize=10.5,fontweight="bold",color=c)
    for i,(k,t) in enumerate(items):
        box(ax,x0+i*1.17,1.55,1.07,1.2,c)
        ax.text(x0+i*1.17+.535,2.35,f"LBL {k}",ha="center",fontsize=11.5,fontweight="bold",color=c)
        ax.text(x0+i*1.17+.535,1.88,t,ha="center",va="center",fontsize=9.5)
ax.text(.1,1.0,"Internal: V (speed prompt, km/h to m/s), Z (results display)",fontsize=9.5,color=GREY)
ax.text(.1,.55,"Flag 1 set: the braking programs also display the stopping distance in 40 ft bus lengths (12.192 m)",fontsize=9.5,color=GREY)
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

# 4 Sight distance
speeds=np.arange(30,101,10); R,F=2.5,0.35
re=speeds/3.6*R; br=(speeds/3.6)**2/(2*g*F)
fig,ax=plt.subplots(figsize=(9,4.4)); ax.grid(axis="x",visible=False)
ax.bar(speeds,re,width=6.5,color=GREEN,alpha=.85,label=f"Reaction: V × R  (R = {R} s)")
ax.bar(speeds,br,bottom=re,width=6.5,color=BLUE,alpha=.85,label=f"Braking: V² ÷ 2g(F + S)  (F = {F}, S = 0)")
for s_,t in zip(speeds,re+br): ax.text(s_,t+2,f"{t:.0f}",ha="center",fontsize=9)
ax.set_xticks(speeds); ax.set_xlabel("Speed (km/h)"); ax.set_ylabel("Distance (m)"); ax.set_ylim(0,210)
ax.legend(frameon=False,loc="upper left",fontsize=9.5)
ax.set_title("Stopping Sight Distance with LBL S",loc="left"); save(fig,"sight_distance")

# 5 Tail swing diagram
O,A,C=3.4,30,1.0
fig,ax=plt.subplots(figsize=(8.5,5.4)); ax.set_aspect("equal"); ax.axis("off")
ax.set_xlim(-6.5,5.2); ax.set_ylim(-2.6,4.2)
ax.plot([-6.5,5.2],[-C,-C],color=INK,lw=2.5); ax.text(-6.4,-C-.35,"Curb line",ha="left",fontsize=10)
ax.add_patch(Rectangle((-6.0,0),6.0,2.5,fc="#eef1f4",ec=GREY,lw=1.5,ls="--")); ax.text(-3.0,1.25,"Bus before the turn",ha="center",color=GREY,fontsize=10)
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
ax.text(-6.4,-2.2,f"K = O·sin A − C = {O*math.sin(th)-C:.2f} m past the curb line (positive = the tail crosses it)",fontsize=10.5,fontweight="bold",color=RED)
ax.text(-6.4,4.0,"Tail Swing with LBL K",fontsize=13,fontweight="bold",va="center")
save(fig,"tail_swing")

# 6 Passenger load
W=6500; N=np.arange(0,91); pct=N*86/W*100
fig,ax=plt.subplots(figsize=(9,4.2))
ax.plot(N,pct,color=BLUE,lw=2.4); ax.fill_between(N,pct,100,where=pct>100,color=RED,alpha=.15,lw=0)
ax.axhline(100,color=RED,ls="--",lw=1.3); ax.text(1,103,f"Weight limit W = {W:,} kg",fontsize=10,color=RED)
nmax=W//86
for n,c in ((60,BLUE),(nmax,ORANGE)):
    ax.plot(n,n*86/W*100,"o",color=c,ms=9,zorder=5); ax.annotate(f"{n} passengers: {n*86:,} kg, {n*86/W*100:.1f}%",xy=(n,n*86/W*100),xytext=(-12,10) if n==nmax else (10,-18),textcoords="offset points",ha="right" if n==nmax else "left",fontsize=10,color=c)
ax.set_xlim(0,90); ax.set_ylim(0,125); ax.set_xlabel("Passengers N"); ax.set_ylabel("Percentage of W (%)")
ax.set_title("Passenger Load with LBL W (86 kg per passenger)",loc="left"); save(fig,"passenger_load")

# 7 Buses required
H=np.arange(5,31); cyc=70; need=cyc/H
fig,ax=plt.subplots(figsize=(9,4.2))
ax.plot(H,need,color=GREY,lw=1.5,ls="--",label="(P + L) ÷ H")
ax.step(H,np.ceil(need-1e-9),where="mid",color=BLUE,lw=2.4,label="Buses to schedule (rounded up)")
ax.plot(15,cyc/15,"o",color=ORANGE,ms=9,zorder=5); ax.annotate("H = 15 min: 4.67 → 5 buses",xy=(15,cyc/15),xytext=(17,8.5),fontsize=10,color=ORANGE,arrowprops=dict(arrowstyle="->",color=ORANGE))
ax.set_xlim(5,30); ax.set_ylim(0,15); ax.set_xlabel("Headway H (minutes)"); ax.set_ylabel("Buses")
ax.legend(frameon=False,loc="upper right",fontsize=9.5)
ax.set_title("Buses Required with LBL B (paddle 60 min + layover 10 min)",loc="left"); save(fig,"buses_required")
