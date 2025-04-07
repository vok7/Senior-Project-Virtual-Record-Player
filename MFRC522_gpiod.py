import time
import gpiod
from gpiod.line import Direction, Value

class MFRC522:
    NRSTPD = 25  # Reset pin (BCM numbering)
    
    # Constants for MFRC522
    PCD_IDLE = 0x00
    PCD_AUTHENT = 0x0E
    PCD_RECEIVE = 0x08
    PCD_TRANSMIT = 0x04
    PCD_TRANSCEIVE = 0x0C
    PCD_RESETPHASE = 0x0F
    PCD_CALCCRC = 0x03
    
    # MFRC522 Commands
    PICC_REQIDL = 0x26
    PICC_REQALL = 0x52
    PICC_ANTICOLL = 0x93
    PICC_SELECTTAG = 0x93
    PICC_AUTHENT1A = 0x60
    PICC_AUTHENT1B = 0x61
    PICC_READ = 0x30
    PICC_WRITE = 0xA0
    PICC_DECREMENT = 0xC0
    PICC_INCREMENT = 0xC1
    PICC_RESTORE = 0xC2
    PICC_TRANSFER = 0xB0
    PICC_HALT = 0x50
    
    # Status codes
    MI_OK = 0
    MI_NOTAGERR = 1
    MI_ERR = 2
    
    # MFRC522 Registers (truncated for brevity - include all from original)
    CommandReg = 0x01
    CommIEnReg = 0x02
    # ... (include all other registers from original)

    def __init__(self, dev='/dev/spidev0.0', speed=1000000, rst_pin=25):
        """Initialize the MFRC522 with gpiod"""
        self.NRSTPD = rst_pin
        
        # Initialize GPIO
        self._setup_gpiod()
        
        # Initialize SPI
        self._setup_spi(dev, speed)
        
        self.MFRC522_Init()
    
    def _setup_gpiod(self):
        """Setup gpiod for reset pin with version compatibility"""
        try:
            # Try new API first (gpiod v2.0+)
            self.chip = gpiod.Chip('gpiochip0')
            self.reset_line = self.chip.get_line(self.NRSTPD)
            
            # Modern API (v2.0+)
            line_settings = gpiod.line_settings()
            line_settings.direction = Direction.OUTPUT
            line_settings.output_value = Value.ACTIVE
            
            line_config = gpiod.line_config()
            line_config.add_line_settings([self.NRSTPD], line_settings)
            
            request = gpiod.request_lines(
                consumer="MFRC522",
                config=line_config
            )
            self.reset_request = request
        except AttributeError:
            try:
                # Fallback to v1.5 API
                self.chip = gpiod.Chip('gpiochip0', gpiod.Chip.OPEN_BY_NAME)
                self.reset_line = self.chip.get_line(self.NRSTPD)
                
                config = gpiod.line_request()
                config.consumer = "MFRC522"
                config.request_type = gpiod.line_request.DIRECTION_OUTPUT
                self.reset_line.request(config=config)
            except AttributeError:
                # Fallback to oldest API
                self.reset_line = self.chip.get_line(self.NRSTPD)
                self.reset_line.request(consumer="MFRC522", type=gpiod.LINE_REQ_DIR_OUT)
            
            self.reset_line.set_value(1)
    
    def _setup_spi(self, dev, speed):
        """Setup SPI communication using spidev"""
        try:
            import spidev
            spi = spidev.SpiDev()
            spi.open(0, 0)  # Bus 0, Device 0
            spi.max_speed_hz = speed
            spi.mode = 0
            return spi
        except ImportError:
            print("spidev not found. Using dummy SPI interface.")
            return DummySPI()
    
    def cleanup(self):
        """Clean up GPIO and SPI resources"""
        try:
            if hasattr(self, 'reset_request'):
                self.reset_request.release()
            elif hasattr(self, 'reset_line'):
                self.reset_line.set_value(1)
                self.reset_line.release()
            if hasattr(self, 'chip'):
                self.chip.close()
        except Exception as e:
            print(f"Error during cleanup: {e}")
        
        if hasattr(self, 'spi'):
            self.spi.close()
    
    # Include all the original MFRC522 methods unchanged:
    # MFRC522_Reset, Write_MFRC522, Read_MFRC522, SetBitMask, 
    # ClearBitMask, AntennaOn, AntennaOff, MFRC522_ToCard,
    # MFRC522_Request, MFRC522_Anticoll, MFRC522_Init
    
    def MFRC522_Reset(self):
        self.Write_MFRC522(self.CommandReg, self.PCD_RESETPHASE)
    
    def Write_MFRC522(self, addr, val):
        self.spi.xfer2([(addr << 1) & 0x7E, val])
    
    def Read_MFRC522(self, addr):
        val = self.spi.xfer2([((addr << 1) & 0x7E) | 0x80, 0])
        return val[1]
    
    # ... (include all other original methods exactly as they were)


class DummySPI:
    """Dummy SPI interface for testing"""
    def xfer2(self, data):
        print(f"SPI write: {data}")
        return [0]*len(data)
    
    def close(self):
        pass
