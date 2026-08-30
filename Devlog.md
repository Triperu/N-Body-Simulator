
# N-Body Gravitation engine,various methods.

Free Fall: 
I first wanted to learn how classes really work while working on a useful Project.
I defined Particle class, aas an object with own position, velocity ([2,] arrays) and mass (float). 
However, as I already had mass and velocity, I decided to define its kinetic energy (kinE) there too.
In order to update Particle's attributes I defined an update function using Euler Cromer's method (v+=a*dt, then p+= v*dt).
Physics engine class simulates the time-lapse evolution on a time array called times, where the step from one value to another defines dt, and copies velocities and positions on arrays with a simple loop as in this case I only used a constant acceleration and particles didn't interact with each other.

 Gravitation: 
Here, I wanted to implement the universal law of gravitation in a way that the particles could interact with each other, updating them with superposition by using the acceleration each particle has after the force balance to update. 
Here it isn't that simple, so I had to divide part of the code to define the calcForces function, so I could calculate the acceleration of each particle, acknowledging its position. It receives a list of particle objects, and for every one of them, it iterates with the rest of the particles, except with itself (if i==j : continue)
first calculating the distance between both particles as a vectorial r_vec and then the norm r. Calcforces returns an accelerations array, one for each particle.

Calcforces is called in the time loop of PhysicsEngine.simulate, and one time before to perform the first update. 
I had a problem with trajectory shapes, because for a n-length times array I always received n-1 positions and velocities.
I introduced the Euler method with update Euler on the class Particle. I added the potential energy in calcforces and kinetic energy in simulate, so I could receive an array with the total energy of the system to check if it really conserves the energy. Then I added an update_Verlet, who should be structured differently, as the position is calculated like in the MRUA, while velocity is calculated with the acceleration's median before and after this step (dt(old_a+new_a)/2). So it requires saving an old acceleration and the new acceleration, and then dclaring old_a = new_a to avoid calling calcforces again. It had a bug right here, because I didn't update the kinetic energy on Verlet update, which I noticed when energy graphics didn't correspond to what is expected physically. I found another bug trying the solar system case, because I used the same particles array to call every method. To do this correctly you need either four different arrays or a function. That's what I use to make sure you're creating a new array each time you call a new method.
I added Runge Kutta 4's method as a separate case like I did with Verlet.

