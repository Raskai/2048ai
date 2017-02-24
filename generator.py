score = 0

def generateRight():
	f = open('right.txt', 'w')
	for n in range(0,16):
		for m in range(0,16):
			for l in range(0,16):
				for k in range(0,16):		
					row = [int(n),int(m),int(l),int(k)]	
					def move():
						for f in range(2,-1,-1):
							if row[f+1] == 0:
								row[f+1] = row[f]
								row[f] = 0
					def merge():
						for f in range (2,-1,-1):
							if row[f] == row[f+1] and row[f] != 0:
								row[f] = 0
								row[f+1] = row[f+1]+1
					move()
					move()
					merge()
					move()
					value = row[3] + (row[2]<<4) + (row[1]<<8) + (row[0]<<12)
					f.write(str(value))
					f.write(" ")

def generateRightScores():
	f = open('rightScores.txt', 'w')
	for n in range(0,16):
		for m in range(0,16):
			for l in range(0,16):
				for k in range(0,16):			
					row = [int(n),int(m),int(l),int(k)]
					global score
					score = 0
					def move():
						for f in range(2,-1,-1):
							if row[f+1] == 0:
								row[f+1] = row[f]
								row[f] = 0
					def merge():
						for f in range (2,-1,-1):
							if row[f] == row[f+1] and row[f] != 0:
								row[f] = 0
								row[f+1] = row[f+1]+1
								global score
								score += 2**row[f+1]
					move()
					move()
					merge()
					move()
					f.write(str(score))
					f.write(" ")

def generateLeft():
	f = open('left.txt', 'w')
	for n in range(0,16):
		for m in range(0,16):
			for l in range(0,16):
				for k in range(0,16):				
					row = [int(n),int(m),int(l),int(k)]	
					def move():
						for f in range(1,4,1):
							if row[f-1] == 0:
								row[f-1] = row[f]
								row[f] = 0
					def merge():
						for f in range (1,4,1):
							if row[f] == row[f-1] and row[f] != 0:
								row[f] = 0
								row[f-1] = row[f-1]+1
					move()
					move()
					merge()
					move()
					value = row[3] + (row[2]<<4) + (row[1]<<8) + (row[0]<<12)
					f.write(str(value))
					f.write(" ")

def generateLeftScores():
	f = open('leftScores.txt', 'w')
	for n in range(0,16):
		for m in range(0,16):
			for l in range(0,16):
				for k in range(0,16):
					row = [int(n),int(m),int(l),int(k)]
					global score
					score = 0
					def move():
						for f in range(1,4,1):
							if row[f-1] == 0:
								row[f-1] = row[f]
								row[f] = 0
					def merge():
						for f in range (1,4,1):
							if row[f] == row[f-1] and row[f] != 0:
								row[f] = 0
								row[f-1] = row[f-1]+1
								global score
								score += 2**row[f-1]
					move()
					move()
					merge()
					move()
					f.write(str(score))
					f.write(" ")

generateRight()
generateRightScores()
generateLeft()
generateLeftScores()