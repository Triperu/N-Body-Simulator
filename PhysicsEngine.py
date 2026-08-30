import numpy as np
from calcforces import calcforces
from Particle import Particle

class PhysicsEngine:
    
    def __init__(self, method):
            self.method=method
    
    def simulate(self, particles, times):
 
        if self.method =="verlet":
            trajectories = [[p.position.copy()] for p in particles]
            velocities = [[p.velocity.copy()] for p in particles]
            potE=0
            
            accelerations, potE = calcforces(particles)
            tot_kinE= [sum(p.kinE for p in particles)]
            tot_potE=[potE]
 
            for it in range (1,len(times)):
                
                dt=(times[it])-times[it-1]
                
  
 
                  
                for k, (particle,acceleration) in enumerate(zip(particles,accelerations)):
                
                    particle.update_pos_verlet(acceleration,dt)
                    trajectories[k].append(particle.position.copy())
                    velocities[k].append(particle.velocity.copy())
            
 
                accelerationsnew, potE= calcforces(particles)
                for particle, old_a, new_a in zip(particles, accelerations, accelerationsnew):
                    particle.update_vel_verlet(old_a, new_a, dt)
                
                kinE=sum(p.kinE for p in particles)
                tot_kinE.append(kinE)
                tot_potE.append(potE)
                
                accelerations=accelerationsnew
            
            
        elif self.method == "rk4":
            trajectories = [[p.position.copy()] for p in particles]
            velocities = [[p.velocity.copy()] for p in particles]
 
            accelerations, potE = calcforces(particles)
            tot_kinE= [sum(p.kinE for p in particles)]
            tot_potE=[potE]
 
            for it in range (1,len(times)):
                dt=(times[it])-times[it-1]
 
                pos = [p.position.copy() for p in particles]
                vel = [p.velocity.copy() for p in particles]
 
                k1_a, _ = calcforces(particles, pos)
                k1_v = vel
 
                pos_k2 = [pos[i]+0.5*dt*k1_v[i] for i in range(len(particles))]
                k2_a,_ = calcforces(particles, pos_k2)
                k2_v = [vel[i]+0.5*dt*k1_a[i] for i in range(len(particles))]
 
                pos_k3 = [pos[i]+0.5*dt*k2_v[i] for i in range(len(particles))]
                k3_a, _ = calcforces(particles, pos_k3)
                k3_v = [vel[i]+0.5*dt*k2_a[i] for i in range(len(particles))]
 
                pos_k4 = [pos[i]+dt*k3_v[i] for i in range(len(particles))]
                k4_a, _  = calcforces(particles, pos_k4)
                k4_v = [vel[i]+dt*k3_a[i] for i in range(len(particles))]
 
                for i, particle in enumerate(particles):
                    particle.update_rk4(k1_v[i], k2_v[i], k3_v[i], k4_v[i],
                                         k1_a[i], k2_a[i], k3_a[i], k4_a[i], dt)
                    trajectories[i].append(particle.position.copy())
                    velocities[i].append(particle.velocity.copy())
 
                accelerations, potE = calcforces(particles)
                kinE=sum(p.kinE for p in particles)
                tot_kinE.append(kinE)
                tot_potE.append(potE)
 
 
        else:
            trajectories = [[p.position.copy()] for p in particles]
            velocities = [[p.velocity.copy()] for p in particles]
            
            accelerations, potE = calcforces(particles)
            tot_kinE= [sum(p.kinE for p in particles)]
            tot_potE=[potE]
 
        
            if self.method == "euler":
                update = Particle.update_euler
            elif self.method == "euler_cromer":
                update = Particle.update_eulercromer
            else:
                raise ValueError(f"Unknown method: {self.method}")
        
 
        
            for it in range (1,len(times)):
                dt=(times[it])-times[it-1]
                  
                for k, (particle,acceleration) in enumerate(zip(particles,accelerations)):
                
                    update(particle,acceleration,dt)
                    trajectories[k].append(particle.position.copy())
                    velocities[k].append(particle.velocity.copy())
                    
 
                accelerations, potE = calcforces(particles)
                kinE=sum(p.kinE for p in particles)
                        
                tot_kinE.append(kinE)
                tot_potE.append(potE)  
                
                
                
                    
        tot_kinE=np.array( tot_kinE)
        tot_potE=np.array(tot_potE)
            
        energy= tot_kinE + tot_potE
                    
        
        
        return trajectories, velocities, energy