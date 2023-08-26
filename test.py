from helper import utils

text = utils.read_file("./static/data.txt")

def convert_wyr(s:str)->tuple[str,str]:
    # Splitting by 'rather' and 'or' 
    splits = s.split('Would you rather')[-1].split(' or ')
    
    # If splitting is successful
    if len(splits) == 2:
        # Stripping leading/trailing spaces and punctuation
        x = splits[0].strip().strip('?')
        y = splits[1].strip().strip('?')
        return (x, y)
    else:
        return (None, None)
        

dataset = []
for line in text.split("\n"):
    optA, optB = convert_wyr(line)
    if optA and optB:
        dataset.append({
            "option_a":optA,
            "option_b":optB
        })
    
utils.write_json("./static/dataset.json", dataset)