from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def enviar_mensaje_whatsapp(numeros, mensaje, repeticiones=10):
    # Configurar opciones de Chrome
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-media-stream")  # Deshabilitar acceso a micrófono
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.media_stream_mic": 2,  # Bloquear micrófono
        "profile.default_content_setting_values.media_stream_camera": 2,  # Bloquear cámara
        "profile.default_content_setting_values.notifications": 2  # Bloquear notificaciones
    })
    
    try:
        # Inicializar el navegador
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        for numero in numeros:
            try:
                # Construir y abrir la URL directa del chat con el mensaje
                url = f'https://web.whatsapp.com/send?phone={numero}&text={mensaje}'
                driver.get(url)
                
                print(f"\nAccediendo al chat del número: {numero}")
                print("Por favor, escanea el código QR si es necesario")
                
                # Enviar el mensaje múltiples veces
                for i in range(repeticiones):
                    try:
                        # Esperar a que se cargue el botón usando la clase específica
                        boton_enviar = WebDriverWait(driver, 60).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-tab="11"]'))
                        )
                        
                        # Esperar un momento adicional
                        time.sleep(2)
                        
                        # Intentar hacer clic en el botón
                        print(f"Intentando enviar mensaje {i+1}/{repeticiones}...")
                        driver.execute_script("arguments[0].click();", boton_enviar)
                        
                        print(f"Mensaje {i+1} enviado a {numero}")
                        
                        # Esperar y preparar siguiente mensaje
                        time.sleep(2)
                        if i < repeticiones-1:  # Si no es el último mensaje
                            driver.get(f'https://web.whatsapp.com/send?phone={numero}&text={mensaje} ({i+2}/{repeticiones})')
                            
                    except Exception as e:
                        print(f"Error al enviar el mensaje {i+1}: {str(e)}")
                        continue
                
                print(f"Todos los mensajes enviados a {numero}")
                time.sleep(3)
                
            except Exception as e:
                print(f"Error con el número {numero}: {str(e)}")
                continue
        
    except Exception as e:
        print(f"Error general: {str(e)}")
    
    finally:
        # Esperar antes de cerrar
        time.sleep(5)
        # Cerrar el navegador
        try:
            driver.quit()
        except:
            pass
        print("\nProceso finalizado")

if __name__ == "__main__":
    # Lista de números con código de país
    numeros_destino = [
        "573025052005"
    ]
    
    mensaje = "¡Hola! Este es un mensaje de prueba automatizado"
    
    # Puedes ajustar el número de repeticiones aquí
    repeticiones = 10
    
    print("Iniciando el proceso de envío de mensajes...")
    enviar_mensaje_whatsapp(numeros_destino, mensaje, repeticiones)