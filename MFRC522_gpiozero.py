import time
from gpiozero import OutputDevice
import spidev

class MFRC522:
    NRSTPD = 25  # Reset pin (BCM numbering)
    
    # Constants (same as original)
    PCD_IDLE = 0x00
    # ... (include all other constants from original)

    def __init__(self, dev='/dev/spidev0.0', speed=1000000, rst_pin=25):
        """Initialize the MFRC522 with GPIO Zero"""
        self.NRSTPD = rst_pin
        
        # Initialize GPIO Zero for reset pin
        self.reset_pin = OutputDevice(self.NRSTPD, active_high=False, initial_value=True)
        
        # Initialize SPI
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)  # Bus 0, Device 0
        self.spi.max_speed_hz = speed
        self.spi.mode = 0
        
        self.MFRC522_Init()
    
    def cleanup(self):
        """Clean up resources"""
        self.reset_pin.close()
        self.spi.close()
    
    def MFRC522_Reset(self):
        self.Write_MFRC522(self.CommandReg, self.PCD_RESETPHASE)
    
    def Write_MFRC522(self, addr, val):
        self.spi.xfer2([(addr << 1) & 0x7E, val])
    
    def Read_MFRC522(self, addr):
        val = self.spi.xfer2([((addr << 1) & 0x7E) | 0x80, 0])
        return val[1]
    
    # ... (include all other original methods unchanged)
    
    def MFRC522_Init(self):
        """Initialize the MFRC522"""
        self.reset_pin.off()
        time.sleep(0.01)
        self.reset_pin.on()
        time.sleep(0.01)
        
        self.MFRC522_Reset()
        
        self.Write_MFRC522(self.TModeReg, 0x8D)
        self.Write_MFRC522(self.TPrescalerReg, 0x3E)
        self.Write_MFRC522(self.TReloadRegL, 30)
        self.Write_MFRC522(self.TReloadRegH, 0)
        
        self.Write_MFRC522(self.TxAutoReg, 0x40)
        self.Write_MFRC522(self.ModeReg, 0x3D)
        self.AntennaOn()
