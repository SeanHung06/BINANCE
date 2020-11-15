def retreive_Position():
    Position = open('./Signal/Position.txt', 'r')   
    pos =  Position.read()
    Position.close()
    return pos 

def Update_Position(Update):
    Position = open('./Signal/Position.txt', 'w')   
    Position.write(Update)