# showing a command line interface demo
import math
from Encryptions.KeyFunctions import bit_decomp_matrix
from Encryptions.KeyFunctions import load_parameters
import numpy as np
import json
from colorama import Fore, Back, Style
from Encryptions.Encryption import EncryptNumber
from Encryptions.Decryption import DecryptNmber

params=load_parameters()

# addition of two cipher text matrices
def Addition(ct1,ct2):
    return ct1+ct2

def Multiplication(ct1,ct2):
    q=params['q']
    l=math.ceil(math.log2(q))
    bdm=bit_decomp_matrix(ct1,l)
    return np.dot(bdm,ct2)

if __name__=="__main__":
    chioce=1
    while chioce!=3:
        print("Choose one of the following")
        print("\t1 : Homomorphic addition ")
        print("\t2 : Homomorphic multiplication")
        print("\t3 : Exit")

        chioce=int(input("Enter your choice : "))
        
        if chioce==1:
            a=int(input("Enter number 1: "))
            b=int(input("Enter number 2: "))
            Enca=EncryptNumber(a)
            Encb=EncryptNumber(b)
            print("Encrytped number 1 : ")
            print(Fore.BLUE+json.dumps(Enca.tolist()))
            print(Fore.RESET)
            print("Encrytped number 2 : ")
            print(Fore.BLUE+json.dumps(Encb.tolist()))
            print(Fore.RESET)
            result=Addition(Enca,Encb)
            print("Result of Added cipher text : ")
            print(Fore.GREEN+json.dumps(result.tolist()))
            print(Fore.RESET)
            print(f"Decrypted addition result : {DecryptNmber(result)}")

        elif chioce==2:
            a=int(input("Enter number 1: "))
            b=int(input("Enter number 2: "))
            Enca=EncryptNumber(a)
            Encb=EncryptNumber(b)
            print("Encrytped number 1 : ")
            print(Fore.BLUE+json.dumps(Enca.tolist()))
            print(Fore.RESET)
            print("Encrytped number 2 : ")
            print(Fore.BLUE+json.dumps(Encb.tolist()))
            print(Fore.RESET)
            print("Result of Multiplied cipher text : ")
            result=Multiplication(Enca,Encb)
            print(Fore.GREEN+json.dumps(result.tolist()))
            print(Fore.RESET)
            print(f"Decrypted Multiplication result : {DecryptNmber(result)}")

        else : 
            print("Good bye !!!")