#########################################################
# Author : Pratik Anand   							    #
# email : pratik          							    #
# Script to generate a social graph with a given degree #
#########################################################


import sys
import time
import datetime
import random
import math
import json
# import numpy as np

VERBOSE = False          # turn it on to print every edge creation
DEBUG = False
FLOATING_POINT_PRECISION = 3
GOAL_THRESHOLD = 2
MAX_TRIALS_GRAPH = 10**6   # 1 million
logfile = ""

if DEBUG is True :
    now = datetime.datetime.now()
    log_time = now.strftime("%I:%M%p on %B %d, %Y")
    try :
        logfile = open("/tmp/social_graph_log_"+log_time, 'w')
    except IOError:
        showErrorMsg('I/O_ERROR', "Cannot create log file")



'''
Prints a string to console and log file too (optional)
'''
def printString(string, log=False  ) :
    print(string)
    if log:
        logfile.write(string + "\n" )

'''
Remove node from set of candidate nodes whose degree count is complete, so that
there are less misses in the loop (accuracy is increased)
It can remove two nodes (which form an edge) at once from candidate nodes.
It can also check removal of single node from candidate nodes
'''
def remove_from_candidate_nodes(rem_degree_count, index_A, index_B = -1) :
    if (index_B != -1) and rem_degree_count[index_A][1] == 0 and rem_degree_count[index_B][1] == 0  :
        # the reason for this is that , we don't want to keep track of changing
        # indices as we delete the two nodes
        # hence, we delete the node with highest index, so this won't affect the index of
        # node with lower index and then we delete the lower index node
        max_index = max(index_A, index_B)
        min_index = list({index_A, index_B} - {max_index})[0] #fancy sets
        del rem_degree_count[max_index]
        del rem_degree_count[min_index]

    elif rem_degree_count[index_A][1] == 0 :
        del rem_degree_count[index_A]

    elif (index_B != -1) and rem_degree_count[index_B][1] == 0 :
        del rem_degree_count[index_B]


'''
This is the main function of the whole script which creates graph(s)
At first, to ensure a connected graph is created, edges are added between all nodes so that there is a circle with each node with 2 degrees
Action peformed in loop:
	Pick up two nodes between [0...NODES] randomly based on SEED
	Check if there is an edge between them, if not create an edge, else skip
	Edge is created by adding entry in dictionory with key as smaller node and value is a set where bigger node is added
	The whole operation is run in multiple of (NODES*(DEGREES-2)) as given by Multiplier
	If all the nodes in the graph has the given degrees, write the graph output in UEL file
FILE_NAME_PREFIX is the prefix with which UEL/histogram file will be saved. Other parts of the file name are
in the format of prefix.node.degree.seed.multiplier_graphiter for UEL
'''
def create_network(nodes, degrees, seed, multiplier, do_clustering_coefficient, do_create_UEL_file, file_name_prefix) :
    start_time = time.time()
    if verifyInput( nodes, degrees, seed, multiplier, do_clustering_coefficient, do_create_UEL_file, file_name_prefix) == False :
        return False, {}

    if seed == -1:
        seed = random.random()
    file_name = getFileName( file_name_prefix, nodes, degrees, seed, multiplier )

    #seeding
    random.seed(seed)
    graphs = MAX_TRIALS_GRAPH

    string = "Running with the arguments"+\
     " Nodes:{}, Degrees:{}, Seed:{}, Graphs:{}, Multiplier:{}, Do Clustering Coeff:{}, Do create UEL file :{}, File name prefix:{}\
     ".format(nodes, degrees, seed, graphs, multiplier, do_clustering_coefficient, do_create_UEL_file, file_name )

    # printString(string, DEBUG)
    final_degrees = {}
    cumulative_avg_degree = 0

    for m in range(graphs) :

        edges = {}
        rem_degree_count = []

        #create a seq circle out of nodes to have connected graph
        for node in range(nodes) :
            if node == nodes - 1 :
                # if VERBOSE :
                #     printString("Adding edge between {} and {}".format( "0", str(node) ), DEBUG  )
                edges[0].add(node)
            else :
                # if VERBOSE :
                #     printString("Adding edge between {} and {}".format( str(node), str(node+1) ), DEBUG  )
                edges[node] = {node+1}

        for x in range(nodes) :
            rem_degree_count.append([x, (degrees-2)])  #each node is stored as a list of Node id, Degree count

		#remove all nodes from candidate nodes which have exhausted their degree count, necessary only for edge case of degree=2
        for node_indx in reversed( range( len(rem_degree_count) ) ) :
            remove_from_candidate_nodes( rem_degree_count, node_indx )



        #rest of the processing
        for i in range( int( math.ceil(multiplier * nodes * (degrees - 2)/2) )) :
            if not rem_degree_count :
                break

            index_A = random.randrange(0, len(rem_degree_count))
            index_B = random.randrange(0, len(rem_degree_count))
            node_A = rem_degree_count[ index_A ][0]
            node_B = rem_degree_count[ index_B ][0]

            if node_A == node_B :            #can't have self edge
                continue

            min_node = min(node_A, node_B)
            max_node = list({node_A, node_B} - {min_node})[0] #fancy sets

            if min_node in edges :
                if max_node in edges[min_node] :     # edge already exists
                    continue
                else :
                    # if VERBOSE :
                    #     printString("Adding edge between {} and {}".format( str(min_node), str(max_node) ), DEBUG  )
                    edges[min_node].add( max_node )  #adding to set

            else :
                # if VERBOSE :
                #    printString("Adding edge between {} and {}".format( str(min_node), str(max_node) ), DEBUG  )
                edges[min_node] = {max_node}  #set

            rem_degree_count[index_A][1] = rem_degree_count[index_A][1] - 1
            rem_degree_count[index_B][1] = rem_degree_count[index_B][1] - 1

            remove_from_candidate_nodes( rem_degree_count, index_A, index_B )


        #print degree_count
        sum = 0
        count = 0
        for x in rem_degree_count :
            sum = sum + (degrees - x[1])

        count  = nodes - len(rem_degree_count)
        sum = sum + count * degrees
        avg_degree = (1.0 * sum)/nodes
        cumulative_avg_degree = cumulative_avg_degree + avg_degree
        # printString("Running for {} iteration".format(m+1), DEBUG)
        # printString("Avg degrees {}".format(avg_degree), DEBUG)
        if do_clustering_coefficient is True:
            calculate_neighbors_clustering_coefficient(m, nodes, edges)

        # printString("Nodes with full cardinality : {}, nodes with not : {}".format( count, nodes - count ), DEBUG)
        # printString("Fraction of nodes with full cardinality : {}, nodes with not : {}".format( (1.0 * count)/nodes, (1.0 * (nodes - count))/nodes ), DEBUG)

        if (nodes == count) or (areOddNodeDegrees(nodes, degrees) and (nodes - count <= GOAL_THRESHOLD))  :
            # printString("Found a valid graph {} at {} iteration".format("within goal threshold" if areOddNodeDegrees(nodes, degrees) else "" , m+1), DEBUG)
            '''
            if there are existing nodes with incomplete cardinality, this prints them out
            In a bug free case, it will only print anything when n and k are both odd
            because otherwise rem_degree_count would be empty
            '''
            # for left_out_node, left_out_degrees in rem_degree_count :
            #     printString("Remaining Node : {}, degree: {}".format(left_out_node, left_out_degrees), DEBUG)
            '''
             Writing to a file
             -------------------
            '''
            # print("\n")
            # print(edges)
            # print("\n")
            if 1 < 2:
                try :
                    thefile = open(file_name+"_" + str(m), 'w')
                except IOError:
                    showErrorMsg('I/O_ERROR', "Cannot create UEL file")
                    return
                for node in range(nodes) :
                    if node == nodes-1 :  #last node's adjacency list will be empty
                        continue
                    neighbors = set(edges[node])
                    for n in neighbors :
                        node_neighbor_data =  str(node) + " " + str(n) #UEL format => node neighbour \n node neighbour \n
                        # print(node_neighbor_data)
            toReturn = {}
            for node in edges:
                if node not in toReturn:
                    toReturn[node] = set()
                for edgenode in edges[node]:
                    if edgenode not in toReturn:
                        toReturn[edgenode] = set()
                    toReturn[node].add(edgenode)
                    toReturn[edgenode].add(node)

            print("\n")
            print(toReturn)
            print("\n")

            return True, toReturn

        # printString("#"*80, DEBUG)

    time_taken_s = round(time.time() - start_time, FLOATING_POINT_PRECISION)
    # printString("Time taken in seconds : {}".format(time_taken_s), DEBUG)
    return False, {}


'''
It also calculates clustering coefficient if it is given as an argument using an optimal traversal
Every node stores neighbors greater than itself. So, for any given node x, the neighboring nodes which are greater
can be found from adjacency list. For the rest, it will start travelling from x-1 node till 1 and add it to a set
of neighbors. Now for clustering coefficient, it each node in set is quickly checked against the new node to
compute if they have a connection, adding to calculatin of clustering coefficient.
'''
def calculate_neighbors_clustering_coefficient(iteration, nodes, edges) :
    clustering_coeff_count = []
    #finding clustering coefficient
    for node in range(nodes) :
        if node in edges : #should not run for largest node as its edges list would be empty here
            neighbors = set(edges[node])   #getting bigger neighbors first (already sorted because it is a set), for optimality
            coeff = 0
            for n1 in range(len(neighbors)) :
                for n2 in range(n1+1, len(neighbors)) :
                    if n2 in edges[n1] :
                        coeff = coeff + 1
        else:
            neighbors = set()  #empty set

        #should run for every node, including the largest
        #for other neighbors, smaller than the number
        for n in range(node-1,-1, -1) :
            if node in edges[n] :                                     #it is a neighbor, hurrah
                common = len(edges[n] & neighbors)
                if common > 0 :                                      #some common nodes are there
                     coeff = coeff + common
                neighbors.add(n)                                      #for optimal results, so that smaller number will match against this node
        '''
        It is decided to change UEL format by not having redundant edeges shown
        '''
        '''
        if create_UEL_file_freq > 0 and (iteration % create_UEL_file_freq == 0): #only create file on 1st/ 3rd / 4th run of the outer loop as per arg given
            for n in neighbors :
                UEL_data.append( str(node) + " " + str(n) )  #UEL format => node neighbour \n node neighbour \n
        '''
        total_coeff = len(neighbors)
        clustering_coeff = round((1.0 * coeff)/ total_coeff,  FLOATING_POINT_PRECISION )     #rounding to 2 floating points
        clustering_coeff_count.append( clustering_coeff )

    clustering_sum = 0
    for x in clustering_coeff_count :
        clustering_sum = clustering_sum + x
    printString("Avg clustering coefficient {}".format((1.0 * clustering_sum)/nodes), DEBUG)

'''
Return the desired filename in the correct format of prefix.node.degree.seed.multiplier
'''
def getFileName(prefix, nodes, degrees, seed, multiplier) :
    return '{}.n.{}.d.{}.s.{}.m.{}'.format(prefix, nodes, degrees, seed, multiplier)
'''
A graph with complete cardinality is mathematically impossible for odd nodes and odd degrees
If n and k are both odd, it is considered as a special case.
This functon checks whether the running arguments belong to this special case
'''
def areOddNodeDegrees(node, degrees) :
    return node % 2 != 0 and degrees % 2 != 0


'''
Create error message based on type of error
'''
def showErrorMsg( type_of_error, string ) :
    if type_of_error == 'INVALID_ARGUMENT' :
        printString( "Invalid argument provided " + string )
    elif type_of_error == 'I/O_ERROR' :
        printString( "File error has occurred " + string )
    else :
        printString( "Unknown error has occurred " + string )

'''
Input validation code , called from createGraph() so that it gets called no matter how the script is being used
'''
def verifyInput( nodes, degrees, seed, multiplier, do_clustering_coefficient, do_create_UEL_file, file_name_prefix) :
    if nodes < 1 :
        showErrorMsg( 'INVALID_ARGUMENT', " Node should be an integer greater than 0 " )
    elif degrees < 2 or degrees >= nodes :
        showErrorMsg( 'INVALID_ARGUMENT', " Degree should be an integer between 2 and nodes - 1 " )
    elif type(seed) is not int and type(seed) is not float :
        showErrorMsg( 'INVALID_ARGUMENT', " Seed should be an integer or a float " )
    elif multiplier < 0 :
          showErrorMsg( 'INVALID_ARGUMENT', " Multiplier should be greater than 0 " )
    elif type(do_clustering_coefficient) is not bool :
        showErrorMsg( 'INVALID_ARGUMENT', " argument on whether to calculate clustering coeff is not provided as boolean" )
    elif type(do_create_UEL_file) is not bool :
           showErrorMsg( 'INVALID_ARGUMENT', " UEL file creation is not provided as boolean " )
    elif type(file_name_prefix) is not str :
        showErrorMsg( 'INVALID_ARGUMENT', " file name prefix is not a string" )
    else :
        return True

    return False


if __name__ == '__main__' :
    if len(sys.argv) > 1 :
        nodes = int(sys.argv[1])
        degrees = int(sys.argv[2])
        seed = int(sys.argv[3])
        multiplier = float(sys.argv[4])
        do_clustering_coefficient = True if sys.argv[5] == 'True' else False
        do_create_UEL_file = True if sys.argv[6] == 'True' else False
        file_name_prefix = ""
        if do_create_UEL_file > 0:
            file_name_prefix = sys.argv[7]

        create_network( nodes, degrees, seed, multiplier, do_clustering_coefficient, do_create_UEL_file, file_name_prefix )
    else :
        printString("Provide all the arguments Nodes, Degrees, Seed, Multiplier, Boolean to calculate clustering coeff, Boolean to create UEL file, File name prefix")
        printString("Sample example")
        printString("python social_graph.py 6 3 55 1 True True /home/pratik/Desktop/test")   #prints every graph to file, use 2 to print every second graph
