

import math
import numpy as np
from Encryptions.KeyFunctions import load_parameters
from Encryptions.KeyFunctions import load_public_key
from Encryptions.KeyFunctions import BitDecompositionInverse


# loading parameters
params=load_parameters()

# only required public key to encrypt
publicKey=load_public_key()

def EncryptText(text):
      encrypted_chars=[]
      for ch in text:
          cenc=EncryptNumber(ord(ch))
          encrypted_chars.append(cenc.tolist())

      return encrypted_chars

def EncryptNumber(a):
      # parameters finding
      q=params['q']
      sigma_c=params['sigmaC']
      n=params['n']
      # finding other values
      l=math.ceil(math.log2(q))
      N=2*l
      pk=np.array(publicKey).reshape(1,2)
      
      r=np.random.choice([0,1],size=(N,1))
      e=np.random.normal(30,sigma_c,size=(N,2)).astype(int)%q

      # performing bit composition
      c=a*BitDecompositionInverse(np.eye(N),l)
      
      # adding error
      # c+=np.dot(r,pk)+e
      c=c.astype(int)%q
      
      # return the encrypted matrix
      return c 
