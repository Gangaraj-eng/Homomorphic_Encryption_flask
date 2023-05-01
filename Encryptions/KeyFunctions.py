# function that generates public and private keys
# it use the parameters defined in environment and 
# generates and store keys in environment file

import json
import os
from dotenv import load_dotenv,find_dotenv
from dotenv import set_key
import numpy as np

load_dotenv()

# parameters that are to be used
Parameters={}


def load_parameters():
    # the prime that will be used
    Parameters['q'] =int(os.environ.get('q'))
    # standard devi
    Parameters['sigmaK'] =int(os.environ.get('sigma_k'))
    Parameters['n'] =int(os.environ.get('n'))
    Parameters['sigmaC'] =int(os.environ.get('sigma_c'))
    return Parameters

def Generate_Keys():
    
    # First load the parameters
    load_parameters()

    # starting key generation
    # generating a random value with normal 
    # distribution form a zeromean and given value 
    # sigma k as variance of key
    t=int(np.random.normal(0,Parameters['sigmaK']))
     
    Secret_key=np.array([1,-t])

    # uniform vector generation
    a=int(np.random.uniform(0,Parameters['q']-1))
    # generating a random error
    RandomError=int(np.random.normal(0,Parameters['sigmaK']))% Parameters['q']

    b=a*t+RandomError
    A = [b,a]
    Public_key=np.array(A)

    UpdateKeys(Public_key,Secret_key)

def UpdateKeys(Public_key,Secret_key):
    
    dot_env_file=find_dotenv()
    
    Public_key=json.dumps(Public_key.tolist())
    Secret_key=json.dumps(Secret_key.tolist())

    set_key(dot_env_file,'PUBLIC_KEY',Public_key)
    set_key(dot_env_file,"SECRET_KEY",Secret_key)

def load_public_key():
    pk=os.environ.get("PUBLIC_KEY")
    pk=json.loads(pk)
    return pk

def load_secret_key():
    sk=os.environ.get("SECRET_KEY")
    sk=json.loads(sk)
    return sk


# return bitdecomposition of integer i
def bitDecomposition(i:int,l:int):
    bd=np.zeros((l,1))
    for x in range(l):
        if i&(1<<x)!=0:
            bd[x]=1

# returns bit decomposition of 2d matrix
def bit_decomp_matrix(c,l):
    n,m=c.shape
    bd=np.zeros((n,m*l))
    for i in range(n):
        for j in range(m):
            for x in range(l):
                if c[i,j]&(1<<x)!=0:
                  bd[i,j*l+x]=1
    return bd

# Get alpha matrix
def get_alpha(y,l):
    alpha=np.zeros((y*l,y))
    for j in range(y):
        for i in range(l):
            alpha[j*l+i,j]=2**i
    return alpha


# return inverse of bit decomposition
def BitDecompositionInverse(mat,l):
    # collecting the dimensions 
    n=mat.shape[0]
    m=mat.shape[1]
    alpha_mat=get_alpha(m//l,l)
    bdi=np.dot(mat,alpha_mat)
    return bdi

# call this function when you need to generate new keys
# Generate_Keys()





