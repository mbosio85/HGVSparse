import sys
import re
ID = 0

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False


def two_to_parse(Parts,offset= 0):
    # check for parentheses
    # if there's a parentesis adapt the logic to the part
    # IF '?' or '*' is there :
        # ?_*1000 -->   will be 1000 - offset
        #  1000?  -->   will be 1000 + offset
    # Else : keep the number
    # btw characters like '+' and '_' are removed from the scope
    vals = ['?','=']
    if '(' in Parts[0]:
        begin = Parts[0].split('(')[1].split(')')[0]
    else:
        begin = Parts[0]
        
    if '(' in Parts[1]:
        ending = Parts[1].split('(')[1].split(')')[0]
    else:
        ending = Parts[1]
    
    if any([x in vals for x in begin]):
        # there are '?' or * in the part to parse
        begin=begin.replace('?','').replace('*','').replace('+','')
        tmp = begin.split('_')
        # Keep the max value in case of (a_B)_( )dup
        if RepresentsInt(tmp[1]):
            begin = tmp[1]
        else :
            begin = str(int(begin.split('_')[0]) + offset)
    elif '_' in begin :
        begin = str(int(begin.split('_')[1]) + offset)

#       # Keep the min value for beginning
#        if RepresentsInt(tmp[0]):
#            begin = tmp[0]
#        else :
#            begin = str(int(begin.split('_')[1]) - offset)
#    elif '_' in begin :
#        begin = str(int(begin.split('_')[0]) - offset)

    if any([x in vals for x in ending]):
        # there are '?' or * in the part to parse
        ending=ending.replace('?','').replace('*','').replace('+','')
        tmp = ending.split('_')
        # Keep the min value for ending
        if RepresentsInt(tmp[0]):
            ending = tmp[0]
        else:
            ending = str(int(ending.split('_')[1]) - offset)
    elif '_' in ending :
        ending = str(int(ending.split('_')[0]) ) #take the min value when xxx_(a_b)dup
#        #keep max value for ending
#        if RepresentsInt(tmp[1]):
#            ending = tmp[1]
#        else:
#            ending = str(int(ending.split('_')[0]) + offset)
#    elif '_' in ending : 
#        ending = str(int(ending.split('_')[1]) ) #take the min value when xxx_(a_b)dup
    return '_'.join([begin,ending])
        
def one_to_parse(variant,offset=10):
    vals = ['?','=']
    variant= variant.split('(')[1].split(')')[0]
    ending = variant.split('_')[1]
    
    
    
    if any([x in vals for x in variant]):
        # there are '?' or * in the part to parse
        #this just stays tge same because it's something like (?_100del)
        value = str(int(ending) - offset)
    return '_'.join([value,ending])
    



print "This tool is required to put variants directly in format HGVS without uncertainty to be used later with hgvs parser.py and produce a VCF"
print "Status\tID\toriginal variant\tParsed variant\tVCF variant"
with open(sys.argv[1]) as rd:
    for line in rd:
        ID +=1 
        # For us it's not interesting at the moment the allel specific annotation
        # So we will remove the '[]'
        # and also substitute (;) with ;
        #print ID
        #Step 1 Isolate the genomic region 
        region='NC_000023.11:g.'
        if region in line:
            pass
        elif 'NM_004992.3:c.' in line:
            region ='NM_004992.3:c.'
        else:
            print 'adjust the script because only supports %s and %s as regions '%(region, 'NM_004992.3:c.')
            print 'exiting'
            print line
            raise

        variants   = line.strip().split(region)[1].replace('[','').replace(']','').replace('(;)',';').split(';')
        #print variants
        
        #Now _ variant by variant
        # Variant is composed of   Part1, Part2 and Type (e.g. delinsXXX)
        # The format is : Part1_Part2Type
        # Whenever we have uncertainty about one of the Parts, the part  should be
        # bewteen parenthesis (Part1)_(Part2)Type
        #print variants
        for i in range(0,len(variants)):
            FinalID = "S%d_%d"%(ID,i+1)
            try:
                #Part1,Part2 = variants[i].split('_')
                r = re.compile(r'(?:[^_(]|\([^)]*\))+')
                
                Parts =  r.findall(variants[i])
                
                #print Parts
                
                
                
                if len(Parts) ==2 :
                  tmp = two_to_parse(Parts)
                elif len(Parts) == 1 and '(' in Parts[0] and ')' in Parts[0]:
                  tmp = one_to_parse(Parts[0])
                else:                
                  print "KK\t%s\t%s\t%s"%(FinalID,variants[i],''.join([region,variants[i]])) # nothing I can do here
                  continue
                   
                #now we have the tmp string which is START_END
                # we have to print out region,start_end,type
                try:
                    type_var = variants[i].split('_')[-1].split(')')[1]
                except:
                    type_var =''
                #print variants[i]
#                if '154032268G>A' in variants[i]:
#                    print variants[i]
#                    print FinalID
#                    print region
#                    print Parts
#                    raise
                
                
                print "OK\t%s\t%s\t%s"%(FinalID,''.join([region,variants[i]]),''.join([region,tmp,type_var] ))
               
               
            except:
                print "KO\t%s\t%s\t%s"%(FinalID,''.join([region,variants[i]]),variants[i])
                #print 'error'
                #raise

        
        
