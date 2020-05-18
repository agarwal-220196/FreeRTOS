"""
Partitionned EDF using PartitionedScheduler.
"""
from simso.core.Scheduler import SchedulerInfo
from simso.utils import PartitionedScheduler
from simso.schedulers import scheduler

@scheduler("simso.schedulers.P_RM")
class P_RM(PartitionedScheduler):
    def init(self):
        PartitionedScheduler.init(
            self, SchedulerInfo("simso.schedulers.RM_mono"))

    def packer(self):
        # First Fit
        cpus = [[cpu, 0] for cpu in self.processors]
        
        #get the length of CPU
        CPUnums = len(cpus)
        print "CPU num: ", numCPUs
        #initialize array of tasks
        tasks = [0]*CPUnums
        
        URM = 0.0
        
        U = 0.0
        
        for task in self.task_list:
            #m = cpus[0][1]
            j = 0
            # Find the processor with the lowest load.
            for i, c in enumerate(cpus):
                #calculating the URM for present and previous number of task
                URM = (tasks[i]+1.0)*((pow(2.0, 1/(tasks[i]+1.0))) - 1.0)
                
                #calculating the utilization 
                U = (c[1] + (task.wcet / task.period))
                
                if U < URM:
                    j=i
                    break
                
                #if c[1] < m:
                #    m = c[1]
                #    j = i
            
            tasks[j] = tasks[j] + 1
            # Affect it to the task.
            self.affect_task_to_processor(task, cpus[j][0])

            # Update utilization.
            cpus[j][1] += float(task.wcet) / task.period
        return True
