
import csv,sys, os, pandas, requests, pickle, argparse

base="http://amp.pharm.mssm.edu/Harmonizome/api/1.0/gene_set/"
parser = argparse.ArgumentParser(description='Get a list of nodes from the user and build a TF-network from the node list.')
parser.add_argument("nodes", help="Full path to your file name",type=argparse.FileType('r'))
parser.add_argument('-s', action="store_true", default=False)

args = parser.parse_args()



filename=args.nodes

def node_parser(filename):
    file = args.nodes
    reader = csv.reader(filename)
    nodes =[row for row in reader]
    nodes = [item for sublist in nodes for item in sublist]
    file.close()
    return nodes

nodes=node_parser(filename);

print(nodes)


def main():
    python_network_builder(nodes);
    






        





























    #TRANSFAC curated 
def transfac_builder(nodes):
     transfac_target_dict={}
     for node in nodes:
         transfac_target_dict[node]=transfac_targets(node)[node]
     with open("super.transfac", "wb") as f:
            pickle.dump(transfac_target_dict, f, pickle.HIGHEST_PROTOCOL)
     
     
     return transfac_target_dict
def transfac_targets(node):
     TRANSFAC="/TRANSFAC+Curated+Transcription+Factor+Targets"
     url=requests.get(base+node+TRANSFAC)
     if url.status_code!=200:
         return {node:"NULL"}
     transfac={node:set()}
     if "associations" in url.json():
         for i in url.json()["associations"]:
             if i["gene"]["symbol"] in nodes:
                 transfac[node].add(i["gene"]["symbol"])
         
         return transfac
     else:
         return{node:"0"}



#ENCODE
def encode_builder(nodes):
         encode_target_dict={}
         for node in nodes:
             encode_target_dict[node]=encode_targets(node)[node]
         with open("super.encode", "wb") as f:
            pickle.dump(encode_target_dict, f, pickle.HIGHEST_PROTOCOL)
         return encode_target_dict



def encode_targets(node):
     base_encode='http://amp.pharm.mssm.edu/Harmonizome/api/1.0/gene_set/'
     encode_url="/ENCODE+Transcription+Factor+Targets"
     url=requests.get(base+node+encode_url)
     if url.status_code!=200:
         return {node:"0"}
     encode={node:set()}
     if "associations" in url.json():
         for i in url.json()["associations"]:
             if i["gene"]["symbol"] in nodes:
                 encode[node].add(i["gene"]["symbol"])
         
         return encode
     else:
         return{node:"0"}
























def master_network_builder(python_file_name,r_file_name):   
     master=merger(python_file_name,r_file_name)
      #Removing self-loops
     master=master[master["source"]!=master["target"]]
     #Let's sort by source and target
     master=master.sort_values(by=['source','target'])
     #Let's remove all duplicate rows. Notice that source and target row might be repeated but with different "sign" 
     master=master.drop_duplicates()
     
     ##Here we collapse all signs so we only keep on arrow per different annotations
     master=master.groupby(['source','target'])['sign'].apply(', '.join).reset_index()
     master.to_csv("master_network.csv")
     return master

def r_network_build(file):
     ##Reading network built from r 
     f=pd.read_csv(file)        
     keep_col = ['source','target','sign']
     return f[keep_col]        
 
 #Reads the network built from pyton into a pandas data frame.
def python_network_build(file):
     f=pd.read_csv(file)
     keep_col = ['source','target','sign']
     return f[keep_col] 
 



def jaspar_builder(nodes):
     jaspar_target_dict={}
     for node in nodes:
         jaspar_target_dict[node]=jaspar_targets(node)[node]
     
     
     with open("super.jaspar", "wb") as f:
        pickle.dump(jaspar_target_dict, f, pickle.HIGHEST_PROTOCOL)
     
     
     return jaspar_target_dict

def jaspar_targets(node):
     jaspar="/JASPAR+Predicted+Transcription+Factor+Targets"
     url=requests.get(base+node+jaspar)
     if url.status_code!=200:
         return {node:"0"}
     jaspar={node:set()}
     if "associations" in url.json():
         for i in url.json()["associations"]:
             if i["gene"]["symbol"] in nodes:
                 jaspar[node].add(i["gene"]["symbol"])
         
         return jaspar
     else:
         return{node:"0"}


def CHEA_builder(nodes):
         CHEA_target_dict={}
         for node in nodes:
             CHEA_target_dict[node]=CHEA_targets(node)[node]
         
         with open("super.CHEA", "wb") as f:
            pickle.dump(CHEA_target_dict, f, pickle.HIGHEST_PROTOCOL)
         
         return CHEA_target_dict


def CHEA_targets(node):
     CHEA="/CHEA+Transcription+Factor+Targets"
     url=requests.get(base+node+CHEA)
     if url.status_code!=200:
         return {node:"0"}
     chea={node:set()}
     if "associations" in url.json():
         for i in url.json()["associations"]:
             if i["gene"]["symbol"] in nodes:
                 chea[node].add(i["gene"]["symbol"])
         
         return chea
     else:
         return{node:"0"}

##Reading from the TRANSFAC predicted database
def transfac_predicted_builder(nodes):
     transfac_predicted_target_dict={}
     for node in nodes:
         transfac_predicted_target_dict[node]=transfac_predicted_targets(node)[node]
         with open("super.transfac_pred", "wb") as f:
            pickle.dump(transfac_predicted_target_dict, f, pickle.HIGHEST_PROTOCOL)
     return transfac_predicted_target_dict
 
 
 
def transfac_predicted_targets(node):
     TRANSFAC_predicted="/TRANSFAC+Predicted+Transcription+Factor+Targets"
     url=requests.get(base+node+TRANSFAC_predicted)
     if url.status_code!=200:
         return {node:"0"}
     transfac_predicted={node:set()}
     if "associations" in url.json():
         for i in url.json()["associations"]:
             if i["gene"]["symbol"] in nodes:
                 transfac_predicted[node].add(i["gene"]["symbol"])
         
         return transfac_predicted
     else:
         return{node:"0"}








def edge_builder(master):
     edges=[("source","target","sign")]
     for key in master:
         for i in master[key]:
             if i != '0':
                 edges.append((key,i,"unknown"))
     return edges


    
def master_dict_builder(nodes):
     #The different dictionaries are currently pickled. See the function loder for details.
     #x=loader()
     #[encode,transfac,jaspar,CHEA,transfac_pred]
     encode=encode_builder(nodes);
     transfac=transfac_builder(nodes);
     jaspar=jaspar_builder(nodes);
     CHEA=CHEA_builder(nodes)
     transfac_pred=transfac_predicted_builder(nodes);
     master={};
     for node in nodes:
         master[node]=set();
     for node in nodes:
         master[node].update(encode[node])
         master[node].update(transfac[node])
         master[node].update(jaspar[node])
         master[node].update(CHEA[node])
         master[node].update(transfac_pred[node])
    
     return master




def merger(python_file_name,r_file_name):
     return pd.concat([python_network_build(python_file_name),r_network_build(r_file_name)])


def python_network_builder(nodes):
    edges=edge_builder(master_dict_builder(nodes))
    with open("python_network.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(edges)
    return "File is called python_network_csv"
def loader():
    with open("super.encode", 'rb') as f:
        encode = pickle.load(f )
    with open("super.jaspar", "rb") as f:
        jaspar=pickle.load(f )
    with open("super.transfac", "rb") as f:
        transfac=pickle.load(f )
    with open("super.CHEA", "rb") as f:
        CHEA=pickle.load(f )
    with open("super.transfac_pred", "rb") as f:
        transfac_pred=pickle.load(f )
    return [encode,transfac,jaspar,CHEA,transfac_pred]


if __name__=="__main__":
    main()
