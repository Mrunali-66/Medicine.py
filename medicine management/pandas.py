import pandas

student_dict={
    "Student": ["Anjali", "Mrunali", "Asmita", "Asmu", "Sonu", "Radha"],
    "Score": [98, 99, 93, 94, 95, 96]
}

student_data_frame = pandas.DataFrame(student_dict)
print(student_data_frame)
