class SimulationOutputVariables(object):
    def __init__(self):

        self.service_times = {
            "inspector_1": [],
            "inspector_2": [],
            "workstation_1": [],
            "workstation_2": [],
            "workstation_3": [],
        }
        self.idle_times = {
            "workstation_1": [],
            "workstation_2": [],
            "workstation_3": [],
        }
        self.block_times = {"inspector_1": [], "inspector_2": []}

        self.products = {
            1: 0,
            2: 0,
            3: 0,
        }

        #every time it tracks it will append each list with the number of components
        self.components = {"c1": [], "c2": [], "c3": []}
        
        #keep track of how long components spend in system
        self.component_times = {"c1": [], "c2": [], "c3": []}

        self.product_times = {1: [], 2: [], 3: []}

        #keep track of occupancy of each buffer
        self.buffers = {"workstation_1": {"c1": []}, "workstation_2": {"c1": [], "c2": []}, "workstation_3": {"c1": [], "c3": []}}
        #keep track of arrival and departure times for each buffer
        self.buffer_times = {"workstation_1": {"c1": []}, "workstation_2": {"c1": [], "c2": []}, "workstation_3": {"c1": [], "c3": []}}

    def add_service_time(self, name, value):
        self.service_times[name].append(value)

    def add_block_time(self, name, value):
        self.block_times[name].append(value)

    def add_idle_time(self, name, value):
        self.idle_times[name].append(value)

    def add_product(self, n):
        self.products[n] += 1
    
    def add_component_time(self, name, value):
        self.component_times[name].append(value)
    
    def add_components(self, components):
        self.components['c1'].append(components['c1'])
        self.components['c2'].append(components['c2'])
        self.components['c3'].append(components['c3'])
    
    def add_buffer(self, name, c, n):
        self.buffers[name][c].append(n)
    
    def add_product_time(self, p, time):
        self.product_times[p].append(time)

    def add_buffer_time(self, name, c, arrival, departure):
        self.buffer_times[name][c].append([arrival, departure])
