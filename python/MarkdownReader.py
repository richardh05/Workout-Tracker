from typing import List

def seperateByH1(mdFile: str) -> List[str]:
    h1_blocks: List[str] = []
    current_block: str = ""
    in_h1_section: bool = False

    for line in mdFile:
                line = line.strip()
                if line.startswith("# "):
                    # Found a new heading 1
                    if current_block:
                        h1_blocks.append(current_block.strip())
                    current_block = line + "\n"  # Start a new block with the heading
                    in_h1_section = True
                elif in_h1_section:
                    current_block += line + "\n"

            # Add the content of the last heading 1 block if it exists
    if current_block:
        h1_blocks.append(current_block.strip())
    return h1_blocks



def extractMD(path: str) -> List[str]:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            myList = seperateByH1(f)

    except FileNotFoundError:
        return []
    except Exception as e:
        return []

    return myList

myList = extractMD("/home/richard/Documents/Obsidian/Personal/02 Projects/Fitness/Exercise.md")
print(myList[0])