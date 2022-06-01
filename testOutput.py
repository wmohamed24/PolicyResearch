
for i in range(1,2):
  x = "Flow" + str(i) + ".txt"
  flow = open(x)
  lines = flow.read()
  print (lines)