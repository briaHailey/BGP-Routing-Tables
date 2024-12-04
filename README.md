# BGP-Routing-Tables
This program extracts information from BGP routing tables and returns
two output files. The first output file, top10.txt, contains the information of the top
10 ASes in terms of the number of neighbors. The second output file, neighbor_count.txt,
lists the neighbor count for all ASes in the descending order based on the number of
neighbors they have. Assumes that the input is a BGP dump file taken in as a command line argument
