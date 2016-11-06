# logicGates
Inkscape extension to assist creating logic circuits symbols, following the 'distinctive shape' of IEEE Std 91/91a-1991 standard.

<img src="docs/images/Examples.png" width="900px"/>

### main features

The main features are

 - you can use up to six inputs for each gate (except NOT gate)
 - each input can be set to be inverted (negated)
 - signal labeling generator with a few commonly used signals pre defined
 - boolean expression editor, with optional LaTeX support and pre defined logic operator functions.

# Installation and requirements

This extension was partially developed in Inkscape 0.48 and partially in 0.91 in Linux (Kubuntu 12.04 and 14.04). It should work on both versions of Inkscape. Also, they should work in different OSs too as long as all requirements are installed.

This extension requires another extension to run, inkscapeMadeEasy <https://github.com/fsmMLK/inkscapeMadeEasy>, which contains several backstage methods and classes.

In order to use logicGates extension, you must also download inkscapeMadeEasy files and put them inside Inkscape's extension directory. Please refer to inkscapeMadeEasy installation instructions. In the end you must have the following files and directories in your Inkscape extension directory.

```
inkscape/extensions/
            |-- inkscapeMadeEasy_Base.py
            |-- inkscapeMadeEasy_Draw.py
            |-- inkscapeMadeEasy_Plot.py
            |-- textextLib
            |   |-- __init__.py
            |   |-- basicLatexPackages.tex
            |   |-- CircuitSymbolsLatexPreamble.tex      <-- add this file to  textextLib  subdirectoy
            |   |-- textext.inx
            |   |-- textext.py
            |
            |-- logicGates.py
            `-- logicGates.inx
```

**Disabling LaTeX support of inkscapeMadeEasy**

Many of the methods implemented in inkscapeMadeEasy project use LaTeX to generate text. To this end I decided to employ the excellent extension **textext** from Pauli Virtanen  <https://pav.iki.fi/software/textext/>. 

LaTeX support via textext extension requires LaTeX typesetting system in your computer (it's free and awesome! =] ), together with a few python modules (pygtk and Tkinter among others). The later might be a problem for non-Linux systems (precompiled inkscape for Windows as OS X don't come with them).

Since many people don't use LaTeX and/or don't have it installed, inkscapeMadeEasy's LaTeX support is now optional. **By default, LaTeX support is ENABLED.**

Please refer to <https://fsmmlk.github.io/inkscapeMadeEasy/#installation-and-requirements> on how to easily disable LaTeX support.

.. warning:: Since disabling LaTeX support is a new feature, this project was not yet extensively checked for misplacements/errors when this support is disabled. Please report any issues you find.

# Usage

This extension is presented in two tabs, **Logic gates** and  **Signals and Expressions**. The extension has two modes of operation. Depending on which tab is on top, the extension will create different elements in your document as soon as you click on `Apply` button (or check `live preview`). The modes are

  1- If `Logic gates` tab is on top, then the extension is set to draw logic gates

  2- If `Signals and Expressions` tab is on top, then the extension is ready to create signals and/or boolean expressions.

### Logic Gates tab

<img src="docs/images/Gates_Tab.png" width="400px"/>

**Gate checkboxes:** You can select the ports to be drawn. More than one gate can be created at once, however they will share the same input configuration (see below)

<img src="docs/images/Gates.png" width="700px"/>

**Number of inputs:** Number of inputs of the gate. This parameter does not affect the NOT gate. You can choose any number between 2 and 6

**Input config:** You can select whether the inputs must be inverted. This field accepts a list of values `1` or `0` separated by commas or spaces, one for each input.
  - 1 stands for regular input
  - 0 stands for inverted input

<img src="docs/images/InputConfig_01.png" width="250px"/>

The first element of this list is associated to the input at the top. If this string has less elements than the number of inputs, the remaining inputs will be set to regular inputs.

Examples:

<img src="docs/images/InputConfig.png" width="700px"/>

### Signals and Expressions tab

<img src="docs/images/Signals_and_expressions_Tab.png" width="400px"/>

This tab is presented in two sections, *Signals* and *Boolean Expressions*. The first create signal nodes to add to your logic circuit. The second creates a text element with a boolean expression.


**Font size:** Adjust the font size for both expression and signal labels.

#### Create Signal section

**Create signal:** Toggles the signal label creator. Check it draw it.

**Signal type:** Allows the selection of one type of signal. You can select a few commonly used signal or select ``Custom`` to customize its label. (see below)

<img src="docs/images/SignalTypes.png" width="800px"/>

**Custom signal label:** Label of the signal. Used only if ``Custom`` is selected in `Signal type`. If LaTeX support is enabled (see `Installation and requirements` section) the text will be inserted in a mathematical environment $...$

**Direction:** Direction of the line segment.

<img src="docs/images/SignalDirection.png" width="400px"/>

**Draw line:** signal line toggle.

<img src="docs/images/SignalLines.png" width="200px"/>

#### Boolean Expressions section

**Create boolean expression:** Toggles the boolean expression creator. Check it draw it.

**Boolean expression:** Boolean expression definition. Commands were created for the basic boolean operators:

<img src="docs/images/BooleanCommands.png" width="450px"/>

> Note: The command ``\NOT`` has one argument and **MUST** be enclosed between ``{ }``

Examples:

<img src="docs/images/BooleanCommands_examples.png" width="800px"/>


# Observations

 - The objects will be created at the center of your screen.

# Examples

<img src="docs/images/Example_minterms.png" width="600px"/>

<img src="docs/images/Example_circuit.png" width="800px"/>


