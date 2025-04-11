import MarkdownLog as ml
import DataClasses as dc
import DatabaseConnector as db

myMD = ml.MarkdownLog("/home/richard/Documents/Obsidian/Personal/02 Projects/Fitness/Exercise.md")
myDays = myMD.days
for d in myDays:
    print(d)
    for x in d.workouts:
        print(x)