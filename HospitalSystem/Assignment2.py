# Berkay Örene 2210356017
import os 

current_dir_path = os.getcwd()
reading_file_name = "doctors_aid_inputs.txt"
reading_file_path = os.path.join(current_dir_path, reading_file_name) # arrange the reading file path
writing_file_name = "doctors_aid_outputs.txt"
writing_file_path = os.path.join(current_dir_path, writing_file_name) # arrange the writing file path

def reading_input_file(): # to read inputs
    with open(reading_file_path, "r") as f:
        global data
        data = (f.readlines())
        global number_of_commands
        number_of_commands = 0 # to learn how much commands or inputs in the input file
        global number_of_create_commands
        number_of_create_commands = 0 # to learn how much create commands in the input file
        for word in data:
            number_of_commands += 1
            if "create" in word:
                number_of_create_commands += 1
reading_input_file()

creating_patients = []
for x in range(number_of_create_commands):
    creating_patients.append([]) # creating multi-dimensional list
# Creating empty lists
patient_names = []
diagnosis_accuraries = []
disease_names = []
disease_incidences = []
treatment_names = []
treatment_risks = []

def create(i): # to create patients
    global current_patient_name
    global patient_name
    patient_name = []
    if "create" in data[i]:
        patient_name = data[i].split(",")[0].split()[1] # selecting patient names
        patient_names.append(patient_name)     
        diagnosis_accuraries.append(str("%.2f" % (float(data[i].split(", ")[1])*100))+"%") # selecting diagnosis accuraries
        disease_names.append(data[i].split(", ")[2]) # selecting disease names
        disease_incidences.append(data[i].split(", ")[3]) # selecting disease incidences
        treatment_names.append(data[i].split(", ")[4]) # selecting treatment names
        treatment_risks.append((data[i].split(", ")[5])[0:4]) # selecting treatment risks
        global current_index
        current_index = patient_names.index(patient_name)
        creating_patients[current_index].append(patient_names[current_index]) # adding into multi dimensional list
        creating_patients[current_index].append(diagnosis_accuraries[current_index]) # adding into multi dimensional list
        creating_patients[current_index].append(disease_names[current_index]) # adding into multi dimensional list
        creating_patients[current_index].append(disease_incidences[current_index]) # adding into multi dimensional list
        creating_patients[current_index].append(treatment_names[current_index]) # adding into multi dimensional list
        creating_patients[current_index].append(treatment_risks[current_index]) # adding into multi dimensional list

current_name = []
def remove(i): # to remove patients
    if "remove" in data[i]:
        global current_name
        current_name = data[i].split(",")[0].split()[1] # who do we want to remove
        global is_it_in_list
        is_it_in_list = False
        if current_name in patient_names:
            is_it_in_list = True
            index = patient_names.index(current_name)
            # Removing the patient
            del creating_patients[patient_names.index(current_name)]
            del patient_names[patient_names.index(current_name)]
            del diagnosis_accuraries[index]
            del disease_names[index]
            del disease_incidences[index]
            del treatment_names[index]
            del treatment_risks[index]
            if current_name in probability_patient_names:
                probability_patient_names.remove(current_name)
                del actual_probabilities[index]
            if current_name in recommendation_patient_names:
                recommendation_patient_names.remove(current_name)

def list(i): # to list patients
    if "list" in data[i]: 
        with open(writing_file_path, "a") as f:  
            f.write("Patient Diagnosis   Disease         Disease     Treatment       Treatment\n")
            f.write("Name    Accurary    Name            Incidence   Name            Risk\n")
            f.write("-------------------------------------------------------------------------\n")
            x = 0
            for a in patient_names:
                x += 1
            for y in range(x):
                number_of_space = 8 - len(creating_patients[y][0]) # calculating how much white space we should print
                number_of_space2 = 16 - len(creating_patients[y][2]) # calculating how much white space we should print
                number_of_space3 = 16 -len(creating_patients[y][4]) # calculating how much white space we should print
                number_of_space = " "*number_of_space # creating whitespaces
                number_of_space2 = " "*number_of_space2 # creating whitespaces
                number_of_space3 = " "*number_of_space3 # creating whitespaces
                f.write(f"{creating_patients[y][0]}{number_of_space}{creating_patients[y][1]}  \t{creating_patients[y][2]}{number_of_space2}{creating_patients[y][3]}   {creating_patients[y][4]}{number_of_space3}{int(float(creating_patients[y][5])*100)}%\n")

probability_patient_names = []
current_probability_patient_name = []
disease_incidence_of_patient = []
actual_probabilities = []
def probability(i): # to calculate the probability
    
    global current_probability_patient_name
    current_probability_patient_name = data[i].split(",")[0].split()[1]
    if current_probability_patient_name in patient_names:
        boolean = False # to prevent calculating the person twice
        if probability_patient_names.count(current_probability_patient_name) == 0: # to prevent calculating the person twice
            probability_patient_names.append(data[i].split(",")[0].split()[1])
            boolean = True
    
        index_of_patient = patient_names.index(current_probability_patient_name)
        disease_incidence_of_patient = disease_incidences[index_of_patient]
        numerator = int(disease_incidence_of_patient.split("/")[0]) # learning numerator of disease incidence
        denominator = int(disease_incidence_of_patient.split("/")[1]) # learning denominator of disease incidence
        diagnosis_accurary_of_patient = float(diagnosis_accuraries[index_of_patient].split("%")[0])/100
        global actual_probability
        actual_probability = (numerator/(((1 - diagnosis_accurary_of_patient)*denominator) + numerator))*100 # calcualating the probability
        actual_probability = float("%.2f" % actual_probability) # adjusting how much decimal number will be after the point
        for_calculating = []
        for_calculating = str(actual_probability)
        if (for_calculating[3]) == "0":
            actual_probability= int(for_calculating[:2]) # it is for removing unnecessary zeros if there is no decimal number after the point       
        if boolean:
            actual_probabilities.append(float(actual_probability))

recommendation_patient_names = []
current_recommendation_patient_name = []
treatment_risk_of_patient = 0
def recommendation(i): # to recommend to patients if they have treatment or not 
    if "recommendation" in data[i]:
        recommendation_patient_names.append(data[i].split(",")[0].split()[1])
        global current_recommendation_patient_name
        current_recommendation_patient_name = data[i].split(",")[0].split()[1] 
        if current_recommendation_patient_name in (patient_names): 
            index = patient_names.index(current_recommendation_patient_name)
            global treatment_risk_of_patient
            treatment_risk_of_patient = (float(treatment_risks[index])*100) # learning treatment risk. I did the rest of it in write function when writing the result
            
def write(i):   # writing the results into a file
    if "create" in data[i]:
        with open(writing_file_path, "a") as f: 
            f.write(f"Patient {patient_name} is recorded.\n")
    if "remove" in data[i]:
        if is_it_in_list: 
            with open(writing_file_path, "a") as f:  
                    f.write(f"Patient {current_name} is removed.\n")
        else:
            with open(writing_file_path, "a") as f:  
                f.write(f"Patient {current_name} cannot be removed due to absence.\n")
    if "probability" in data[i]:
        
        if current_probability_patient_name in patient_names:
            with open(writing_file_path, "a") as f: 
                f.write(f"Patient {current_probability_patient_name} has a probability of {actual_probability}% of having breast cancer.\n")
        else:
            with open(writing_file_path, "a") as f:
                f.write(f"Probability for {current_probability_patient_name} cannot be calculated due to absence.\n")

    if "recommendation" in data[i]:
        if current_recommendation_patient_name in patient_names:
            if treatment_risk_of_patient > actual_probabilities[probability_patient_names.index(current_recommendation_patient_name)]:
                with open(writing_file_path, "a") as f:
                    f.write(f"System suggests {current_recommendation_patient_name} NOT to have the treatment.\n") 
            else:
                with open(writing_file_path, "a") as f:
                    f.write(f"System suggests {current_recommendation_patient_name} to have the treatment.\n")             

        else:
            with open(writing_file_path, "a") as f:
                f.write(f"Recommendation for {current_recommendation_patient_name} cannot be calculated due to absence.\n")

for i in range(number_of_commands):
    if "create" in data[i]:
        create(i)
        probability(i)
        write(i)
    elif "remove" in data[i]:
        remove(i)
        write(i)
    elif "list" in data[i]:
        list(i)
    elif "probability" in data[i]:
        probability(i)
        write(i)
    elif "recommendation" in data[i]:
        recommendation(i)
        write(i)
