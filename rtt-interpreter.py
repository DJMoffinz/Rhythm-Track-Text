import time
import os

#turn the code into something python can understand better. you could just make it run the code right here but idk i want it separated
def parse_rtt(rtt_text):
    events = []
    lines = rtt_text.strip().split('\n')
    tempo = None
    signature = None #not actually implemented properly kinda, just only use 4/4 until i do

    #so yeah again just preprocesses stuff, should be fairly obvious what it does if you read it
    for line in lines:
        if line.startswith('TEMPO'):
            tempo = int(line.split()[1])
        elif line.startswith('SIGNATURE'):
            numerator, denominator = line.split()[1:]
            signature = {'numerator': float(numerator), 'denominator': float(denominator)}
        elif line.startswith('ARROW'):
            direction, beat = line.split()[1:]
            event = {'type': 'arrow', 'direction': direction, 'beat': float(beat)}
            events.append(event)
        elif line.startswith('HOLD'):
            direction, start, end = line.split()[1:]
            event = {'type': 'hold', 'direction': direction, 'start': float(start), 'end': float(end)}
            events.append(event)
    return {'tempo': tempo, 'signature': signature, 'events': events}

#here's the actual interpreter bit
def interpret_parsed(parsed_data):
    tempo = parsed_data['tempo']
    bar_beats, beat_duration = parsed_data['signature']['numerator'], parsed_data['signature']['denominator']
    events = parsed_data['events']

    #small function to convert UDLR to arrow shapes
    def arrow(direction):
        arrow_array = {
            'U': '^',
            'D': 'v',
            'L': '<',
            'R': '>'
        }
        return(arrow_array.get(direction, '?'))
    #make it be the beginning, i should probably move all this type of stuff to the top somewhere
    current_beat = 0.0
    #go through the events
    for event in events:
        match event['type']:
            case 'arrow':
                #wait 'till it's time to do the thing, should make this a function
                while current_beat < event['beat']:
                    time.sleep(60/tempo)
                    current_beat += 1/beat_duration
                    if current_beat == event['beat']:
                        #when it's time, print an arrow and the current beat
                        print(f"{current_beat:<4}",arrow(event['direction']))
                    else:
                        #just print the current beat
                        print(f"{current_beat:<4}")
            case 'hold':
                #this is all the same as the other one except it holds for more than one beat
                while current_beat < event['end']:
                    time.sleep(60/tempo)
                    current_beat += 1/beat_duration
                    if current_beat == event['start']:
                        print(f"{current_beat:<4}",arrow(event['direction']))
                    elif current_beat > event['start']:
                        #print the long bit of the arrow
                        print(f"{current_beat:<4}",'|')
                    else:
                        print(f"{current_beat:<4}")
            case _:
                #tell you you messed up, probably won't need to tell line numbers or whatever cause everything's in order anyway
                print('invalid event',event['type'])

#read a file
def rfile(file):
    with open(file, 'r') as my_file:
        return(my_file.read())

#clear the command line
os.system('cls')

#run the thing
interpret_parsed(parse_rtt(rfile(os.sys.argv[1])))
