# Image-To-Scope-Converter
Raster oscilloscope image generator from an arbitrary bitmap file.
<br/>
<p align="center">
     <img width="600" src="https://github.com/Kononenko-K/Image-To-Scope-Converter/blob/main/pics/slowmo.gif">
</p>

## Overview
The idea behind this project is based on the fact that rapid signal transitions are almost imperceptible on a CRT. Thus, if we make a signal jump with a very short rise/fall time from point A to point B, there will be no visible trace of movement on the display. Here, I use the MCU's DAC to generate horizontal and vertical scan signals, and an open-drain GPIO output to create the sharpest possible edge by shorting the DAC output to ground (which is not ideal, but the DAC's output impedance is relatively high anyway). This allows to return the dot on the screen to the zero position when the pixel is white, enabling the display of a raster image on any 2-channel CRT oscilloscope in XY mode without modifying its circuitry for brightness modulation.

## [Hardware](Hardware)
<p align="center">
    <img width="600" src="https://github.com/Kononenko-K/Image-To-Scope-Converter/blob/main/pics/board.jpg">
</p>

The board features an STM32F405 series MCU, USB-UART converter, USB Type-C connector, negative voltage generator, and a wideband 2-channel operational amplifier. [KiCad project files](/Hardware/PCB) and [PDF documentation](/Hardware/PCB/project.pdf) are avaliable. For correct operation, DACx and PWMx outputs should both be connected to the corresponding Ax pins.

## [Firmware](Firmware)
The firmware is configured to work with a 1 MBd USART speed, 256×256 image resolution, and adjustable frame rate. The MCU receives an 8192-byte array representing XBM-format images with 1 bit per pixel encoding. The frame rate can be adjusted using the button connected to the PB1 pin. A test image is included in the firmware and can be found in [test_im.h](/Firmware/Core/Src/test_im.h). It is displayed immediately after power-on until another image is loaded via UART.
The project is developed using STM32CubeIDE with HAL.

## [Software](Software)
<p align="center">
    <img width="500" src="https://github.com/Kononenko-K/Image-To-Scope-Converter/blob/main/pics/ui.png">
</p>

I developed a Python PyQt5 script for the project GUI that generates properly formatted data from arbitrary images. Here are the [source code](/Software/ui.py) and [requirements](/Software/requirements.txt).

## [Enclosure](/Hardware/Enclosure)
<p align="center">
    <img width="400" src="https://github.com/Kononenko-K/Image-To-Scope-Converter/blob/main/pics/1.png">
    <img width="400" src="https://github.com/Kononenko-K/Image-To-Scope-Converter/blob/main/pics/2.png">
</p>

STL files for the [case](/Hardware/Enclosure/1.stl) and its [cover](/Hardware/Enclosure/2.stl) for 3D printing.

## License
- The **Software** and **Firmware** in this project are licensed under the [MIT License](/Firmware/LICENSE), with the exception of portions of the firmware code that are copyrighted by STMicroelectronics; such portions are subject to the original licensing terms provided by STMicroelectronics.
- The **Hardware** in this project is licensed under the [CERN Open Hardware Licence Permissive (CERN OHL-P)](/Hardware/LICENSE).
