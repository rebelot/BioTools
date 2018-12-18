from schrodinger.application.desmond.packages import traj
import sys

trj = traj.read_traj(sys.argv[1])

f = len(trj)
t0 = trj[0].time
te = trj[-1].time
dt = (te - t0) / f

print()
print(f"    frames: {f}")
print(f"start_time: {t0} ps")
print(f" last_time: {te} ps")
print(f"  interval: {dt:.5f} ps/f", end=" ")

if len(sys.argv) > 2 and sys.argv[2] == "-test":
    test = sum((trj[i+1].time - trj[i].time) / dt for i in range(len(trj) - 1))/f
    print(f"(consistency: {test:.2%})")
else:
    print()

# t = t0 + dt * f
# frames = (te - t0) / dt
# dt = (te - t0) / frames
# f = (t - t0) / dt

# if args.time >= 0:
#     print('Nearest frame to time %.2f ps is %d'
#           % (args.time, math.floor((args.time - elapsed_time) / step)))

# if args.frame >= 0:
#     print('Chemical time of frame %d is %.2f ps'
#           % (args.frame, elapsed_time + step * args.frame))

print()
