
First import Net class from core.net  
`from core.net import Net`  
`substrate_network = Net()`  
This create a blank substrate network with no any Node and link.  
`substrate_network.init_bandwidth_capacity(1, 6, 100)`  
This add a new link as well as two node 1 and 6 with bandwidth 100 unit
`substrate_network.init_node_cpu_capacity(1, 100)`  
This add (or change if the node is existed) a node 1 with capacity 100


How to construct an SFC:
1. create two VNFs for src and dst node with cpu request 0
2. set bandwidth request of src out come bandwidth
3. Create a void SFC with src and dst.
4. Create the VNFs need to be installed in SFC.
5. Add VNFs into SFC
6. Connect VNFs from src to dst
7. Set latency request
8. Assign substrate nodes to src and dst vnf in sfc as they should be defined before deployment. 


