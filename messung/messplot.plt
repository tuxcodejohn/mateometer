
set xrange [ 100 : 1900 ]
set yrange [ 0 : 1 ]
set xlabel "frequency in Hz"
set ylabel "Mate fill status in fractions of 500ml"

#set logscale x

#plot "messreihe_d" , 0.95936658171875 - ( 24559.784492173  / x **2)
#plot "messreihe_d" , 0.96 - ( 24560  / x **2)
plot "messreihe_d" , 1 - ( 24560  / x **2)

pause -1
