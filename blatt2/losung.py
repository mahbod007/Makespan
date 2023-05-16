#################################
########## Aufgabe 1 ############
#################################
import random


file = open('scheduling.txt', 'r')

# Read the contents of the file
lines = file.readlines()

# Close the file
file.close()

# Get number of machine
number_of_machines = int(lines[0].replace("m = ", ""))

# Get process time unit for each job
time_unit_of_jobs = []
for line in lines[1:]:
    time_unit_of_jobs.append(int(line.replace("\n", "")))


class Job(object):
    def __init__(self, ind, length):
        self.number = ind
        self.length = length
        self.in_machine = -1

    def __iter__(self):
        return iter(self)

    def __str__(self):
        return "[%s, %s]" % (self.number, self.length)

    def __repr__(self):
        return "[%s, %s]" % (self.number, self.length)

    def __len__(self):
        return self.length

    def __eq__(self, other):
        if self.number != other.number:
            return False
        else:
            return True

    def getNumber(self):
        return self.number

    def getLength(self):
        return self.length


class Machine(object):
    def __init__(self, num):
        self.assigned_jobs = []
        self.number = num  # Machine serial #
        self.span = 0  # Initial makespan

    def __str__(self):
        return "Machine number: %s \n Machine span: %s \n Jobs numbers: %s \n" % (self.number, self.span, self.assigned_jobs)

    def __repr__(self):
        return "Machine number: %s \n Machine span: %s \n Jobs numbers: %s \n " % (self.number, self.span, self.assigned_jobs)

    def __iter__(self):
        return iter(self)

    def retrieveJobsList(self):
        return self.assigned_jobs

    def addJob(self, job):
        self.assigned_jobs.append(job)
        self.span += job.getLength()
        job.in_machine = self.number

    def retrieveJob(self, job):
        return self.assigned_jobs.index(job)

    # removing job from the machine by job number
    def removeJob(self, job):
        self.span -= job.getLength()
        self.assigned_jobs.remove(job)
        job.in_machine = -1


# Creates and returns a machines list
def createMachines(number_of_machines):
    machines = []
    for i in range(0, number_of_machines):
        cur_machine = Machine(i+1)
        machines.append(cur_machine)
    return machines
#print(createMachines(number_of_machines))


def createJobs(time_unit_of_jobs):
    jobs = []
    for i, job in enumerate(time_unit_of_jobs):
        cur_job = Job(i+1, job)
        jobs.append(cur_job)
    return jobs

def weightiestMachine (machines):
    lowest_span = 0
    target_machine_index = -1
    for i, machine in enumerate(machines):
        if machine.span > lowest_span:
            lowest_span = machine.span
            target_machine_index = i
    return machines[target_machine_index]

def swapJobs(machine1, machine2, job1, job2):
    machine1.removeJob(job1)
    machine2.removeJob(job2)
    machine1.addJob(job2)
    machine2.addJob(job1)
    return

def moveJob(orgine_machine, target_machine, job):
    orgine_machine.removeJob(job)
    target_machine.addJob(job)


def swapPossibility(machine1_span, machine2_span, job1_length, job2_length, max_span):
    desired_machine1_span = machine1_span - job1_length + job2_length
    desired_machine2_span = machine2_span - job2_length + job1_length
    if desired_machine1_span < machine1_span and desired_machine2_span < machine2_span and desired_machine1_span < max_span and desired_machine2_span < max_span:
        return True
    else:
        False

def movePossiblility(orgin_machine_span, target_machine_span, candidate_job_length, max_span):
    desired_target_machine_span  = target_machine_span + candidate_job_length
    if orgin_machine_span > desired_target_machine_span and desired_target_machine_span < max_span:
        return True
    else:
        return False


#################################
########## Aufgabe 2 ############
#################################
machines = createMachines(number_of_machines)
jobs = createJobs(time_unit_of_jobs)

# Assign first round
for i, machine in enumerate(machines):
    if machine.span == 0:
        machine.addJob(jobs[i])

# Soreted remaining Job Assignment
for job in jobs:
    if job.in_machine == -1:
        lowest_span = float('inf')
        target_machine_index = -1
        for i, machine in enumerate(machines):
            if machine.span < lowest_span:
                lowest_span = machine.span
                target_machine_index = i 
        machines[target_machine_index].addJob(job)
 
print("Aufgabe2: ")
print(weightiestMachine(machines))


#################################
########## Aufgabe 3 ############
#################################
improvement_possible = 1
while improvement_possible == 1:
    weightiest_machine = weightiestMachine(machines)
    max_span = weightiest_machine.span
    for job_index, job in enumerate(weightiest_machine.assigned_jobs):
        for machine in machines:
            if movePossiblility(weightiest_machine.span, machine.span, job.getLength(), max_span):
                improvement_possible = 1 
                moveJob(weightiest_machine, machine, job)
                break
            else:
                for job2_index, job2 in enumerate(machine.assigned_jobs):
                    if swapPossibility(weightiest_machine.span, machine.span, job.getLength(), job2.getLength(), max_span):
                        improvement_possible = 1
                        swapJobs(weightiest_machine, machine, job, job2)
                        break
                    else:
                        improvement_possible = 0
    if weightiestMachine(machines).span != max_span:
        improvement_possible = 1
    else:
        improvement_possible = 0


print("Aufgabe3: ")
print(weightiestMachine(machines))


#################################
########## Aufgabe 4 ############
#################################
for i in range(5):
    machines = createMachines(number_of_machines)
    jobs = createJobs(time_unit_of_jobs)
    random.shuffle(jobs)

    # Assign first round
    for i, machine in enumerate(machines):
        if machine.span == 0:
            machine.addJob(jobs[i])

    # Soreted remaining Job Assignment
    for job in jobs:
        if job.in_machine == -1:
            lowest_span = float('inf')
            target_machine_index = -1
            for i, machine in enumerate(machines):
                if machine.span < lowest_span:
                    lowest_span = machine.span
                    target_machine_index = i
            machines[target_machine_index].addJob(job)

    print("Aufgabe4: ")
    print("Max Mahine: ")
    print(weightiestMachine(machines))

    improvement_possible = 1
    while improvement_possible == 1:
        weightiest_machine = weightiestMachine(machines)
        max_span = weightiest_machine.span
        for job_index, job in enumerate(weightiest_machine.assigned_jobs):
            for machine in machines:
                if movePossiblility(weightiest_machine.span, machine.span, job.getLength(), max_span):
                    improvement_possible = 1
                    moveJob(weightiest_machine, machine, job)
                    break
                else:
                    for job2_index, job2 in enumerate(machine.assigned_jobs):
                        if swapPossibility(weightiest_machine.span, machine.span, job.getLength(), job2.getLength(), max_span):
                            improvement_possible = 1
                            swapJobs(weightiest_machine, machine, job, job2)
                            break
                        else:
                            improvement_possible = 0
        if weightiestMachine(machines).span != max_span:
            improvement_possible = 1
        else:
            improvement_possible = 0
                     
    print(weightiestMachine(machines))

