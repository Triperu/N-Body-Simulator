import numpy as np

class Particle:
    def __init__(self, mass, position, velocity):
            self.mass=mass
            self.position=np.array(position,dtype=float)
            self.velocity=np.array(velocity,dtype=float)
            self.kinE=0.5*mass*(np.linalg.norm(velocity))**2
 
    
    def update_eulercromer(self, acceleration, dt):
        self.velocity+= np.array(acceleration)*dt
        self.position+= self.velocity*dt
        self.kinE=0.5*self.mass*(np.linalg.norm(self.velocity))**2
    
    def update_euler(self, acceleration, dt):
        self.position+= self.velocity*dt
        self.velocity+= np.array(acceleration)*dt
        self.kinE=0.5*self.mass*(np.linalg.norm(self.velocity))**2
        
    def update_pos_verlet(self,acceleration,dt):
        self.position+=self.velocity*dt+0.5*acceleration*dt**2
        
 
    def update_vel_verlet(self,old_a,new_a,dt):
        self.velocity+= 0.5*(old_a+new_a)*dt
        self.kinE = 0.5*self.mass*(np.linalg.norm(self.velocity))**2
 
    def update_rk4(self, k1_v, k2_v, k3_v, k4_v, k1_a, k2_a, k3_a, k4_a, dt):
        self.position+= (dt/6)*(k1_v+2*k2_v+2*k3_v+k4_v)
        self.velocity+= (dt/6)*(k1_a+2*k2_a+2*k3_a+k4_a)
        self.kinE=0.5*self.mass*(np.linalg.norm(self.velocity))**2
 
