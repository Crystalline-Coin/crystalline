import crystaline.transaction.Signature as sg
import crystaline.transaction.Transaction as tr
import crystaline.public_address.public_address_generator as pa
from ecpy.curves import Point, Curve

CURVE_NAME = 'Ed448'

print("Transaction and Signature Test :")

input_text = ""
transaction = None

while input_text != '0':
    print("please enter :")
    print("   0  -> exit")
    print("   1  -> create transaction")
    print("   2  -> sign transaction")
    print("   3  -> get public key")
    print("   4  -> validate signature with public key")
    print("   5  -> print transaction details in string format(except signature)")
    print("   6  -> print transaction inputs")
    print("   7  -> print transaction outputs")
    print("   8  -> print transaction signature")
    print("   9  -> print transaction data in json format")
    print("   10 -> save transaction to file")
    print("   11 -> load transaction from file")

    input_text = input()

    if input_text == '1' :
        inputs = input("please enter inputs of transaction in list of tuples format : ")
        outputs = input("please enter outputs of transaction in list of tuples format : ")
        
        inputs_of_trans = []
        for tup in inputs.split('),('):
            tup = tup.replace(')', '').replace('(', '').replace('[', '').replace(']', '').replace('"', '').replace("'", '')
            inputs_of_trans.append(tuple(tup.split(',')))

        outputs_of_trans = []
        for tup in outputs.split('),('):
            tup = tup.replace(')', '').replace('(', '').replace('[', '').replace(']', '').replace('"', '').replace("'", '')
            outputs_of_trans.append(tuple(tup.split(',')))
        
        transaction = tr.Transaction(inputs_of_trans, outputs_of_trans, "")

    if input_text == '2' :
        if transaction == None:
            print("Please create a transaction first!")
        else :
            pv_key = int(input("please enter your Private key (integer type) to sign the transaction : "))
            sig = sg.sign(transaction, pv_key)
            transaction.signature = sig

    if input_text == '3' :
        pv_key = int(input("please enter your Private key (integer type) to generate your Public key : "))
        pub_add = pa.PublicAddressGenerator(pv_key)
        pub_key = pub_add.public_key
        print("Your Public key is : " + str(pub_key))

    if input_text == '4' :
        if transaction == None:
            print("Please create a transaction first!")
        elif transaction.signature == "" :
            print("Please sign the transaction first!")
        else : 
            pub = input("please enter your public key : ")
            ls = pub.split(' , ')
            x = ls[0].replace('(', '')
            y = ls[1].replace(')', '')
            pubkey = Point(int(x, base=16), int(y, base=16), Curve.get_curve(CURVE_NAME))
            validation = sg.verify_signature(transaction, pubkey)
            print("Relsult of verifing the transaction with public key : " + str(validation))
    
    if input_text == '5' :
        if transaction == None:
            print("Please create a transaction first!")
        else :
            print("transaction details : " + transaction.get_details())
    
    if input_text == '6' :
        if transaction == None:
            print("Please create a transaction first!")
        else :
            print("transaction inputs : " + str(transaction.input_address))

    if input_text == '7' :
        if transaction == None:
            print("Please create a transaction first!")
        else :
            print("transaction outputs : " + str(transaction.output_address))

    if input_text == '8' :
        if transaction == None:
            print("Please create a transaction first!")
        elif transaction.signature == "" :
            print("Please sign the transaction first!")
        else : 
            print("transaction signature : " + str(transaction.signature))

    if input_text == '9' :
        if transaction == None:
            print("Please create a transaction first!")
        else :
            print("transaction in json format : ")
            js = transaction.to_json()
            print(js)

    if input_text == '10' :
        if transaction == None:
            print("Please create a transaction first!")
        else :
            file_address = input("Please enter a file location to saving transaction : ")
            transaction.save(file_address)

    if input_text == '11' :
        file_address = input("Please enter a file location to load transaction from : ")
        if(transaction == None):
            transaction = tr.Transaction([], [], "")
        transaction.load(file_address)

    print()
