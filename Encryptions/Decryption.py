
import math
import numpy as np
from Encryptions.KeyFunctions import load_parameters
from Encryptions.KeyFunctions import load_secret_key
from Encryptions.KeyFunctions import bit_decomp_matrix
from Encryptions.KeyFunctions import BitDecompositionInverse
from Encryptions.Encryption import EncryptText

# loading parameters
params=load_parameters()

# only secrete key to decrypt
SecretKey=load_secret_key()

def DecryptText(enc_arr):
     textSize=len(enc_arr) 
     result=""
     
     for arr in enc_arr:
           result+=chr(DecryptNmber(np.array(arr)))

     return result

def DecryptNmber(arr):
     # parameters finding
      q=params['q']

     # finding other params
      l=math.ceil(math.log2(q))
      N=2*l

      sk=np.array(SecretKey).reshape(2,1)
      t1=np.dot(arr,sk)
      t2=np.dot(BitDecompositionInverse(np.eye(N),l),sk)

      fin=np.round(t1/t2).astype(int).reshape(-1)%q

      return np.bincount(fin).argmax()
