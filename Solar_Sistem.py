import numpy as np
import time
import matplotlib.pyplot as plt

from Particle import Particle
from PhysicsEngine import PhysicsEngine                                        
                
engine=PhysicsEngine(method="euler")
enginec=PhysicsEngine(method="euler_cromer")
enginever=PhysicsEngine(method="verlet")
enginerk=PhysicsEngine(method="rk4")

def make_solar_system():
    p_sun = Particle(1.989e30, [0, 0], [0, 0])
    p_mercury = Particle(3.301e23, [5.7895e10, 0], [0, 47883.8667])
    p_venus = Particle(4.867e24, [1.0816e11, 0], [0, 35032.8563])
    p_earth = Particle(5.972e24, [1.4960e11, 0], [0, 29788.2298])
    p_mars = Particle(6.417e23, [2.2799e11, 0], [0, 24129.7161])
    p_jupiter = Particle(1.898e27, [7.7837e11, 0], [0, 13059.2364])
    p_saturn = Particle(5.683e26, [1.4267e12, 0], [0, 9645.8123])
    p_uranus = Particle(8.681e25, [2.8710e12, 0], [0, 6799.7961])
    p_neptune = Particle(1.024e26, [4.4983e12, 0], [0, 5432.3182])
    return [p_sun, p_mercury, p_venus, p_earth, p_mars,
            p_jupiter, p_saturn, p_uranus, p_neptune]

labels = ["Sun", "Mercury", "Venus", "Earth", "Mars",
          "Jupiter", "Saturn", "Uranus", "Neptune"]

dt = 86400.0                    # 1 day
t_max = 3600*24*365*1          # 1 year
times = np.arange(0, t_max, dt)



t0=time.perf_counter()
trajectories_e, velocities_e, energye = engine.simulate(make_solar_system(), times)
t1=time.perf_counter(); time_e = t1-t0

t0=time.perf_counter()
trajectories_ec, velocities_ec, energyec = enginec.simulate(make_solar_system(), times)
t1=time.perf_counter(); time_ec = t1-t0

t0=time.perf_counter()
trajectories_ver, velocities_ver, energyver = enginever.simulate(make_solar_system(), times)
t1=time.perf_counter(); time_ver = t1-t0

t0=time.perf_counter()
trajectories_rk, velocities_rk, energyrk = enginerk.simulate(make_solar_system(), times)
t1=time.perf_counter(); time_rk = t1-t0

print(f"euler time:        {time_e:.4f} s")
print(f"euler_cromer time: {time_ec:.4f} s")
print(f"verlet time:       {time_ver:.4f} s")
print(f"rk4 time:          {time_rk:.4f} s")


#trajectories
trajectories_by_method = {
    "euler": np.array(trajectories_e),
    "euler_cromer": np.array(trajectories_ec),
    "verlet": np.array(trajectories_ver),
    "rk4": np.array(trajectories_rk),
}

plt.figure(figsize=(12, 12))
for i, (method, traj) in enumerate(trajectories_by_method.items(), start=1):
    plt.subplot(2, 2, i)
    for k in range(traj.shape[0]):
        plt.plot(traj[k,:,0], traj[k,:,1], label=labels[k], linewidth=1)
    plt.gca().set_aspect("equal")
    plt.title(method)

plt.legend(fontsize=8, loc="center left", bbox_to_anchor=(1.02, 0.5))
plt.suptitle("Trajectories: Solar System "f"T = {t_max/(365*24*3600):.1f} years, dt = {dt/86400:.1f} days")
plt.tight_layout()
plt.savefig("solar system trajectories", dpi=120, bbox_inches="tight")
plt.close()

#energy conservation
npart, nite, _= np.shape(trajectories_ver)



plt.figure(figsize=(8,5))
plt.semilogy(times, abs((energye-energye[0])/energye[0]), label="euler")
plt.semilogy(times, abs((energyec-energyec[0])/energyec[0]), label="eulercromer")
plt.semilogy(times, abs((energyver-energyver[0])/energyver[0]), label="verlet")
plt.semilogy(times, abs((energyrk-energyrk[0])/energyrk[0]), label="rk4")
plt.xlabel("time (s)")
plt.ylabel("|E - E0| (log scale)")
plt.title("Energy conservation relative error: Solar System "f"T = {t_max/(365*24*3600):.1f} years, dt = {dt/86400:.1f} days")
plt.legend()
plt.tight_layout()
plt.savefig("solar system energy conservation", dpi=120)
plt.close()


#execution time
methods = ["euler", "euler_cromer", "verlet", "rk4"]
times_list = [time_e, time_ec, time_ver, time_rk]

plt.figure(figsize=(6,5))
bars = plt.bar(methods, times_list)
for bar, t in zip(bars, times_list):
    plt.text(bar.get_x()+bar.get_width()/2, bar.get_height(),
             f"{t:.3f}s", ha="center", va="bottom")
plt.ylabel("execution time (s)")
plt.title(f"Execution time: Solar System\n" f"T = {t_max/(365*24*3600):.1f} years, dt = {dt/86400:.1f} days")
plt.tight_layout()
plt.savefig("solar system time", dpi=120)
plt.close()

print("\nPlots saved: solar_trajectories.png, solar_energy.png, solar_time.png")
 