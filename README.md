# __Private__Image-To-Scope-Converter
Raster oscilloscope images generator from an arbitrary bitmap file.
<br/>
<p align="center">
     <img width="600" src="https://github.com/Kononenko-K/Image-To-Scope-Converter/blob/main/pics/slowmo.gif">
</p>

## Overview
The idea behind this project is based on the fact that a rapid signal change is almost imperceptible on a CRT. Thus, if we make a signal hop with small rise/fall time from point A to point B there will be no movement traces on the display. Here I use MCU's DAC to generate horisontal and vertical scan signals and open-drain GPIO output to form the sharpest edge possible by shorting DAC output to the ground (which is quite not good but but the output impedance of the DAC is comparatively high anyway). So that I can return the dot on the screen to zero point when the pixel is white. This allows to display a raster image on any 2-channel CRT oscilloscope in XY mode without changing its schematic for brigtness modulation.
## [Hardware](Hardware)
<p align="center">
    <img width="600" src="https://github.com/Kononenko-K/Image-To-Scope-Converter/blob/main/pics/board.jpg">
</p>

The board contains STM32 F405 series MCU, USB-UART converter, Type-C connector, negative voltage generator and wideband 2-channel OP amp. There are [KiCad project](/Hardware), [Gerber files](/Hardware/gerber) and [PDF](/Hardware/project.pdf) avaliable. For correct operation DACx and PWMx should be both connected to Ax pins respectively.

## [Firmware](Firmware)
The firmware is set to work with 1 MBd USART speed, 256x256 image resolution, and adjustable frame rate. The MCU receives an 8192 byte array of basically XMB format images with 1 bit per pixel encoding. The frame rate can be adjusted with the button on PB1 pin. The test image is included in the firmware and can be found in [test_im.h](/Firmware/Core/Src/test_im.h). It will be displayed rignt after power on until another image is loaded through UART. 
The project is made in STM32CubeIDE with HAL.

## [Software](Software)
<p align="center">
    <img width="500" src="https://github.com/Kononenko-K/Image-To-Scope-Converter/blob/main/pics/ui.png">
</p>

I made a python PyQt5 script for the project GUI that can generate properly formatted data from an arbitrary image. Here is the [code](/Software/ui.py) and [requirements](/Software/requirements.txt).

## [Enclosure](Enclosure)
<p align="center">
    <img width="400" src="https://github.com/Kononenko-K/Image-To-Scope-Converter/blob/main/pics/1.png">
    <img width="400" src="https://github.com/Kononenko-K/Image-To-Scope-Converter/blob/main/pics/2.png">
</p>

STL files of the [case](/Enclosure/1.stl) and its [cover](/Enclosure/2.stl) for 3D printing.
