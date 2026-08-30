import numpy as np

def calcforces(particles, positions=None):
    G=6.67E-11
    if positions is None:
        positions = [p.position for p in particles]
 
    accelerations=[]
    potE=0
    for i, particle_i in enumerate(particles):
        
        acceleration=np.zeros(2)
 
        for j, particle_j in enumerate(particles):
            if i == j:
                continue
               
            r_vec= positions[j]-positions[i]
            r=np.linalg.norm(r_vec)
            acceleration += G*particle_j.mass*r_vec/r**3
            potE += ((-G*particle_j.mass*particle_i.mass/r)/2)
        accelerations.append(acceleration)
         
                   
    return accelerations,potE