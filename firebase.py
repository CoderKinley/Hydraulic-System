import pyrebase

class FirebaseConnectivity:
    def __init__(self):
        # initilising the required data for uploading the data
        self.config = {
            "apiKey": "AIzaSyARhmKyZm_BcsEioLHWCK7XP2Gg6RMavN0",
            "authDomain": "pyto-db701.firebaseapp.com",
            "projectId": "pyto-db701",
            "databaseURL": "https://pyto-db701-default-rtdb.firebaseio.com/",
            "storageBucket": "pyto-db701.appspot.com",
            "messagingSenderId": "229412264516",
            "appId": "1:229412264516:web:f2fdafadec99efeef23a11",
            "measurementId": "G-PYES5CSJQ7"
        }

    def connect_firebase(
            self, 
            p_extension, 
            velocity,
            flow_rate, 
            f_extension, 
            power_input, 
            power_output
        ):
        
        try:
            firebase = pyrebase.initialize_app(self.config)
            database = firebase.database()

            piston_data = {
                "Piston_extension": p_extension, 
                "velocity": velocity, 
                "flow_rate" : flow_rate, 
                "force_extension": f_extension, 
                "power_input" : power_input, 
                "power_output" : power_output 
            }

            database.push(piston_data)
            # print("piston extension: " + str(data) + " Velocity: " + str(velocity))
            print("pushed to firebase...")

        except Exception as e:
            print("error! ", str(e))
