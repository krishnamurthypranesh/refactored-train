# refactored-train

Building a python based load balancer to understand how loads are balanced.

# Requirements
## Basic Load Balancing
	- The load balancer should just act as a proxy and forward requests directly to instances.
	- The load balancer should forward requests to the servers with the same headers it received as part of the request.
	- The load balancer should maintain state. Where state is defined as follows:
		- The number of requests served by each instance.
		- The number of requests each instance has queued up for it.
		- The number of requests an instance can serve at a given point of time.
	- Based on state, the load balancer should allocate requests to instances.
	- If instances are running at full capacity, the load balancer should return appropriate message.
	- The load balancer should maintain state of the number of requests which got served this message.
## Autoscaling
	- When all instances or more than n/2 instances are at more than 50% capacity, the load balancer should signal the start of a new instance.
	- This new instance should then be added to the list of available instances and should start accepting requests ASAP.
	- The number of instances at any point should not exceed 10.
	- The number of instances at any point should not fall below 2.
	- If an instance falls below 25% capacity for more than 2 health checks, it must be stopped.
	- Instances will be terminated when the load balancer receives a request to stop the entire process.

# Done
	- Get app server up and running.
	- Write socket for load balancer
# To-do
	- 
