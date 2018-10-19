import sys

def parse_line(line,prot_idx,extra_fields,offset=2):
    ff=line.strip().split('\t')
    if '_' in ff[0]:
      ff[0] = ff[0].split('_')[1]
    ID= ':'.join([ff[0],ff[1],ff[2]])
    gene=ff[3]
    tx = ff[4]
    extra = ff[-1]
    ff.pop()
    ff.insert
    protein_pos = ff[prot_idx]
    #this can be :
    # just number 33
    # N-N
    # ?-N
    # N-?
    # ?
    # -
    start = 'NA'
    end   = 'NA'
    if   '-' in protein_pos:
        if protein_pos =='-':
            pass
        else:
            pp = protein_pos.split('-')
            if pp[0] =='?':
                end   =  int(pp[1])
                start =  max(0,end -offset)
            elif pp[1] =='?':
                start = int(pp[0])
                end   = start + offset
            else: #both numbers
                start = int(pp[0])
                end   = int(pp[1])
            
        
    else :
        #just number
        start = int(protein_pos)
        end   = int(protein_pos)
    
    start = str(start)
    end = str(end)
    
    ## extra fields:
    extra_list= extra.split(';')
    extra_output = ['NA']*len(extra_fields)
    for i in extra_list :
        key = i.split('=')[0]
        if key=='SIFT' or key=='PolyPhen':
            val = i.split('=')[1].split('(')[1].replace(')','')
        else:
            val = i.split('=')[1]
        extra_output[extra_fields.index(key)] = val
    #print extra_output
    ff.extend(extra_output)
    
    
    #Add items
    ff[prot_idx] = end
    ff.insert(prot_idx,start)
    ff.insert(0,ID)
    #add start and end
    outf=ff
    #outf= [ID,gene,tx,start,end]
    
    return outf


prot_idx = 9
with open(sys.argv[1]) as rd:
    extra_fields = []
    switch = False
    for line in rd:
               
        if line.startswith('##') :
            if '## Extra column keys:' in line:
                switch = True
            elif switch:
                extra_fields.append(line.split(' ')[1])

            
        elif line.startswith('#'):
            line = line.replace('#','')
            ff = line.strip().split('\t')
            prot_idx = ff.index('Protein_position')
            ff[prot_idx] = 'Protein_start\tProtein_end'
            ff.pop()
            ff.extend(extra_fields)
            print('ID\t'+'\t'.join(ff))
                                
        else:
            print('\t'.join(parse_line(line,prot_idx,extra_fields)))
