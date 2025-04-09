from typing import List

def seperateByHeader(mdFile: str, header: str) -> List[str]:
    hBlocks: List[str] = []
    current_block: str = ""

    for line in mdFile:
        line = line.strip()
        if line.startswith(header):
            if current_block:
                hBlocks.append(current_block.strip())
            current_block = line + "\n"  # Start a new block with the heading
        elif current_block:  # Only add content if we are within a header's block
            current_block += line + "\n"

    if current_block:
        hBlocks.append(current_block.strip())
    return hBlocks


def getFirstLine (block: str, header: str) -> str:
    lines = block.splitlines()
    if lines and lines[0].startswith(header):
        return lines[0][len(header):].strip()
    else:
        return ""


def extractMD(path: str) -> List[str]:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            days = seperateByHeader(f.readlines(),"# ")
            for day in days:
                 date = getFirstLine(day,"# ")
                 exercises = seperateByHeader(day.splitlines(),"## ")
                 for e in exercises: 
                    exercise_type = getFirstLine(e,"## ")
                    print(exercise_type)

    except FileNotFoundError:
        return []
    except Exception as e:
        return []

    return days

myList = extractMD("/home/richard/Documents/Obsidian/Personal/02 Projects/Fitness/Exercise.md")
#print(myList)
#print(myList[0])