// Definir conexiones y parametros para el control del motor
#define dirPin 12 //pin de direccion (horario o antihorario)
#define stepPin 13 //pin de movimiento (avanza o se detiene)
#define enPin 14 //pin de habilitacion del motor
#define speed 6000 //velocidad del motor
#define origen 3000 //velocidad para volver al origen
#define freno 1000 //mantener el motor frenado 1 seg

void setup() {
  pinMode(stepPin, OUTPUT); //define los pines GPIO como salida
  pinMode(dirPin, OUTPUT);
  pinMode(enPin, OUTPUT);

// Inicia la comunicacion serial con una velocidad de 9600 baudios
  Serial.begin(9600);

// Parte siempre con el motor apagado y sentido horario
digitalWrite(enPin, HIGH); //apaga el motor
digitalWrite(dirPin, LOW); //sentido horario
}

void loop() {

  if (Serial.available()) { //Comprobar si se ha recibido algún dato por el puerto serie
    String input = Serial.readStringUntil('\n'); //Leer la entrada serial
    
    //ESTABLECER SENTIDO DE GIRO
    if (input == "horario") { //Comprobar la entrada serial
      digitalWrite(dirPin, LOW); //establece sentido horario
    } 

    if (input == "antihorario") { //Comprobar la entrada serial
      digitalWrite(dirPin, HIGH); //establece sentido antihorario
    } 

    if (input == "5deg") { //Comprobar la entrada serial
      digitalWrite(enPin, LOW); //enciende el motor
      for (int i = 0; i < 25; i++) { //Dar los pasos indicados
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(speed);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(speed);
        
      }
      delay(freno); //el motor permanece frenado
      digitalWrite(enPin, HIGH); //apaga el motor
    }

    if (input == "10deg") { //Comprobar la entrada serial
      digitalWrite(enPin, LOW); //enciende el motor
      for (int i = 0; i < 50; i++) { //Dar los pasos indicados
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(speed);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(speed);
      }
      delay(freno); //el motor permanece frenado
      digitalWrite(enPin, HIGH); //apaga el motor
    }

    if (input == "20deg") { //Comprobar la entrada serial
      digitalWrite(enPin, LOW); //enciende el motor
      for (int i = 0; i < 100; i++) { //Dar los pasos indicados
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(speed);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(speed);
      }
      delay(freno); //el motor permanece frenado
      digitalWrite(enPin, HIGH); //apaga el motor
    }

    if (input == "30deg") { //Comprobar la entrada serial
      digitalWrite(enPin, LOW); //enciende el motor
      for (int i = 0; i < 150; i++) { //Dar los pasos indicados
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(speed);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(speed);
      }
      delay(freno); //el motor permanece frenado
      digitalWrite(enPin, HIGH); //apaga el motor
    }

    if (input == "45deg") { //Comprobar la entrada serial
      digitalWrite(enPin, LOW); //enciende el motor
      for (int i = 0; i < 225; i++) { //dar los pasos indicados
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(speed);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(speed);
      }
      delay(freno); //el motor permanece frenado
      digitalWrite(enPin, HIGH); //apaga el motor
    }

    if (input == "90deg") { //Comprobar la entrada serial
      digitalWrite(enPin, LOW); //enciende el motor
      for (int i = 0; i < 450; i++) { //dar los pasos indicados
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(speed);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(speed);
      }
      delay(freno); //el motor permanece frenado
      digitalWrite(enPin, HIGH); //apaga el motor
    }

    if (input == "180deg") { //Comprobar la entrada serial
      digitalWrite(enPin, LOW); //enciende el motor
      for (int i = 0; i < 900; i++) { //dar los pasos indicados
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(speed);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(speed);
      }
      delay(freno); //el motor permanece frenado
      digitalWrite(enPin, HIGH); //apaga el motor
    }

    if (input == "360deg") { //Comprobar la entrada serial
      digitalWrite(enPin, LOW); //enciende el motor
      for (int i = 0; i < 1800; i++) { //dar los pasos indicados
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(speed);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(speed);
      }
      delay(freno); //el motor permanece frenado
      digitalWrite(enPin, HIGH); //apaga el motor
    }

    if (input == "origen") { //Comprobar la entrada serial
      digitalWrite(enPin, LOW); //enciende el motor
      digitalWrite(dirPin, HIGH); //establece sentido antihorario
      for (int i = 0; i < 1800; i++) { //dar los pasos indicados
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(origen);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(origen);
      }
      delay(freno); //el motor permanece frenado
      digitalWrite(enPin, HIGH); //apaga el motor
    }
 
  
  }

}


