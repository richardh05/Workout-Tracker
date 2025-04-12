import MarkdownLog as ml
import DataClasses as dc
import DatabaseConnector as db
import pandas as pd

myMD = ml.MarkdownLog("/home/richard/Documents/Obsidian/Personal/02 Projects/Fitness/Exercise.md")
myDays = myMD.days
myWriter = db.DatabaseWriter("/home/richard/Documents/gym")
for d in myDays:
    myWriter.writeDayClass(d)