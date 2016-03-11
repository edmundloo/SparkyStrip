from subprocess import Popen, PIPE, call
import sys

keep_going = True
while(keep_going):
    train = True if input("Training or testing:").lower() == "training" else False
    if train:
        device_name = input("Input 1:speaker, 2:incandescent bulb, 3:CFL, or any consecutive integer (starting from 4 and not skipping any numbers) 'Device Name' that you can remember what device it maps to:")
        assert device_name.isnumeric()
        print("Taking samples to train machine learning model.")
    else:
        device_name = input("Assign a name for the test sample set, ideal naming convention is '<integer 'Device Name'>_test':")
        max_device_name = input("What is the max 'Device Name'? If you haven't added any devices, the default is 3:")
        assert max_device_name.isnumeric()
        print("Taking samples to identify device.")

    call(['python3', 'arduino_mongo.py', 'train' if train else 'test', device_name], shell = True)
    
    if not train:
        call(['python3', 'create_predict_x.py', device_name], shell = True)
        call(['python3', 'device_identification.py', ' '.join([str(x) for x in range(1, int(max_device_name)+1)])], shell = True)
        with open('Y_predict', 'r') as Y:
            detect_count = []
            for line in Y:
                detect_count.append(line.strip())
            print("The Device Name your device identified as is:", max(set(detect_count), key=detect_count.count))
    
    keep_going = True if input("Keep going?")[0].lower() == 't' else False