#!/usr/bin/python



def dataclean(seq,schwelle2=4,killneg=False):
	seq.sort()
	i=0
	if killneg :
		while i< len(seq) and seq[i] < 0:
			i +=1
		seq = seq[i:]
		i=0
	z = map (lambda x : x[0] - x[1] ,zip(seq[:-1],seq[1:]))
	dif , start,end =  0,0,0
	while i < len(z):
		if abs(z[i]) > schwelle2 :
			i += 1
			continue
		j = i+1
		while j < len(z) and ( abs (z[j]) <= schwelle2 ) :
			j +=1
		if ( (j-1 -i) > dif ):
			dif , start , end = (j-1-i) , i , (j-1)
		i+=1
	return seq[start:end]


if __name__ == '__main__':
	a = [0,1,30,32,32,34,200,33,90,32,94,93,300,32,31,50]
	b = dataclean(a)
	print b ,"-->",  int(round(float(sum(b))/len(b))) , "(%f)"% (float(sum(b))/len(b))



