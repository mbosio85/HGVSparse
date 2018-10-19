
import sys 
import itertools
with open(sys.argv[1]) as rd:
 for line in rd:

  print line
  a =  ["".join(x) for _, x in itertools.groupby(line.strip(), key=str.isdigit)]
  print a
  



D  C . . .
3 319780 . GA G . . .
19 110747 . G GT . . .
1 160283 sv1 . <DUP> . . SVTYPE=DUP;END=471362 .
1 1385015 sv2 . <DEL> . . SVTYPE=DEL;END=1387562 .
