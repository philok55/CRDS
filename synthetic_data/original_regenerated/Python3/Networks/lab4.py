"""
Lab 4
NAME: Philo Decroos & Thijs van de Vijver
STUDENT ID: 11752262, 11751185
DESCRIPTION:
This script uses matplotlib to plot the Congestion Window value of a TCP
connection in a time interval. For both the Tahoe and New-Reno implementations
of TCP we will identify the transitions between states in the data and print
them to standard output.
"""
importfileinput
importmatplotlib.pyplotasplt
importnumpyasnp
frommatplotlibimportcollectionsasmc
importmatplotlib.patchesasmpatches
importmath
defmain():
    times=[]
cwnd=[]
segments=[]
colors=[]
forlineinfileinput.input():
        ifline.startswith('#'):
            continue
 x,y=line.split()
times.append(float(x))
cwnd.append(int(y))
 ssthresh=float("inf")
MSS=536
avoidance=False
slow_start=True
fast_recovery=False
foriinrange(len(times)):
        ifavoidance:
            colors.append(tuple([1,0,0,1]))
 eliffast_recovery:
            colors.append(tuple([0,1,0,1]))
 elifslow_start:
            colors.append(tuple([0,0,1,1]))
 ifi==0:
            print(">> Transition at "+str(times[i])+" to slow start. Value of cwnd: "+str(cwnd[i])+".")
continue
 ifcwnd[i]<cwnd[i-1]:
            ssthresh=cwnd[i-1]//2
ifcwnd[i]==MSS:
                colors[i-1]=[1,1,0,1]
print(">> Timeout at "+str(times[i-1])+". Value of cwnd: "+str(cwnd[i-1])+".")
ifnotslow_start:
                    print(">> Transition at "+str(times[i-1])+" to slow start. Value of cwnd: "+str(cwnd[i-1])+".")
 avoidance=False
fast_recovery=False
slow_start=True
 else:
                ifnotfast_recovery:
                    print(">> Transition at "+str(times[i-1])+" to fast recovery. Value of cwnd: "+str(cwnd[i-1])+".")
fast_recovery=True
slow_start=False
avoidance=False
   elifcwnd[i]>ssthresh:
            iffast_recoveryorslow_start:
                ifcwnd[i]==cwnd[i-1]+MSS*math.ceil(MSS/cwnd[i-1]):
                    print(">> Transition at "+str(times[i-1])+" to congestion avoidance. Value of cwnd: "+str(cwnd[i-1])+".")
avoidance=True
fast_recovery=False
slow_start=False
   segments.append([(times[i-1],cwnd[i-1]),(times[i],cwnd[i])])
 segments.pop(0)
colors.pop(0)
lc=mc.LineCollection(segments,colors=colors,linewidths=2)
fig,ax=plt.subplots()
ax.add_collection(lc)
ax.autoscale()
ax.margins(0.1)
avoidance_patch=mpatches.Patch(color=[1,0,0,1],label='congestion avoidance')
slow_start_patch=mpatches.Patch(color=[0,0,1,1],label='slow start')
fast_recovery_patch=mpatches.Patch(color=[0,1,0,1],label='fast recovery')
timeout_patch=mpatches.Patch(color=[1,1,0,1],label='timeout')
plt.legend(handles=[avoidance_patch,slow_start_patch,fast_recovery_patch,timeout_patch])
plt.ylabel('Congestion window')
plt.xlabel('Time')
plt.show()

if__name__=='__main__':
    main()

<EOF>