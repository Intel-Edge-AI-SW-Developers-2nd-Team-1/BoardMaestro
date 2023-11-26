#pip install pybluez
import bluetooth
import time
import threading

def bluetoothsetup():
    serverMACAddress = '98:DA:60:07:A1:3A' #목표 주소
    port = 1    #포트는 1번으로 사용하는 것이 일반적
    socekt = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    socekt.connect((serverMACAddress, port))
    return socekt

def send_data(socket):
    while True:
        message = input('')
        if message.lower() == 'q':
            socket.close()
            break

        # STM32로 메시지 전송
        socket.send(message + "\r\n")

def receive_data(socket):
    while True:
        # STM32로부터 데이터 수신
        data = socket.recv(1024)
        print("Cursor move:", data.decode())  # 수신된 데이터 출력

def main():
    socket = bluetoothsetup()

    try:
        send_thread = threading.Thread(target=send_data, args=(socket,))
        receive_thread = threading.Thread(target=receive_data, args=(socket,))

        send_thread.start()
        receive_thread.start()

        send_thread.join()
        receive_thread.join()
        
    except KeyboardInterrupt:
        pass  # Ctrl+C를 눌러 프로그램을 중지해도 오류가 발생하지 않게 함
    finally:
        socket.close()  # Bluetooth 소켓 닫기

if __name__ == "__main__":
    main()