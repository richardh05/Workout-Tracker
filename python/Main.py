import MarkdownLog as ml
import DataClasses as dc
import DatabaseConnector as db
import pandas as pd

myMD = ml.MarkdownLog("/home/richard/Documents/Obsidian/Personal/02 Projects/Fitness/Exercise.md")
myDays = myMD.days
for d in myDays:
    #print(d)
    for w in d.workouts:
        print(w)
        print(w.sets)            
        for row in w.sets.itertuples():
            print(row)
            index = row[0]  # Index
            value = row.Value
            reps = row.Reps
            print(f"Index: {index}, Value: {value}, Age: {reps}")