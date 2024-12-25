#!/usr/bin/python

import math
import os

import inkscapeMadeEasy.inkscapeMadeEasy_Base as inkBase
import inkscapeMadeEasy.inkscapeMadeEasy_Draw as inkDraw


# print(os.getcwd())
# sys.path.append('./inkscapeMadeEasy')


# ---------------------------------------------
# noinspection PyUnboundLocalVariable,PyDefaultArgument,PyAttributeOutsideInit
class LogicGates(inkBase.inkscapeMadeEasy):
    def __init__(self):
        inkBase.inkscapeMadeEasy.__init__(self)

        self.arg_parser.add_argument("--tab", type=str, dest="tab", default="object")
        self.arg_parser.add_argument("--subTab_sigExp", type=str, dest="subTab_sigExp", default="object")

        self.arg_parser.add_argument("--ANDgate", type=self.bool, dest="ANDgate", default=False)
        self.arg_parser.add_argument("--ORgate", type=self.bool, dest="ORgate", default=False)
        self.arg_parser.add_argument("--XORgate", type=self.bool, dest="XORgate", default=False)
        self.arg_parser.add_argument("--NOTgate", type=self.bool, dest="NOTgate", default=False)
        self.arg_parser.add_argument("--BUFgate", type=self.bool, dest="BUFgate", default=False)
        self.arg_parser.add_argument("--NANDgate", type=self.bool, dest="NANDgate", default=False)
        self.arg_parser.add_argument("--NORgate", type=self.bool, dest="NORgate", default=False)
        self.arg_parser.add_argument("--XNORgate", type=self.bool, dest="XNORgate", default=False)

        self.arg_parser.add_argument("--symbolSize", type=str, dest="symbolSize", default='small')

        self.arg_parser.add_argument("--nInput", type=int, dest="nInput", default=2)
        self.arg_parser.add_argument("--InputTypes", type=str, dest="InputTypes", default='11')

        self.arg_parser.add_argument("--latchType", type=str, dest="latchType", default='none')
        self.arg_parser.add_argument("--latchSize", type=str, dest="latchSize", default='large')
        self.arg_parser.add_argument("--latchSuppressq", type=self.bool, dest="latchSuppressq", default=False)
        self.arg_parser.add_argument("--latchSuppressNOTq", type=self.bool, dest="latchSuppressNOTq", default=False)

        self.arg_parser.add_argument("--latchGate", type=str, dest="latchGate", default='none')
        self.arg_parser.add_argument("--latchGateLogic", type=str, dest="latchGateLogic", default='HIGH')
        self.arg_parser.add_argument("--latchPreset", type=str, dest="latchPreset", default='0')
        self.arg_parser.add_argument("--latchClear", type=str, dest="latchClear", default='0')

        self.arg_parser.add_argument("--signal", type=str, dest="signal", default='GND')
        self.arg_parser.add_argument("--signalVal", type=str, dest="signalVal", default='E')
        self.arg_parser.add_argument("--signalRot", type=float, dest="signalRot", default=0)
        self.arg_parser.add_argument("--signalDrawLine", type=self.bool, dest="signalDrawLine", default=True)

        self.arg_parser.add_argument("--boolExpression", type=str, dest="boolExpression", default='')

    def effect(self):

        so = self.options

        # sets the position to the viewport center, round to next 10.
        position = [self.svg.namedview.center[0], self.svg.namedview.center[1]]
        position[0] = int(math.ceil(position[0] / 10.0)) * 10
        position[1] = int(math.ceil(position[1] / 10.0)) * 10

        # root_layer = self.current_layer
        root_layer = self.document.getroot()
        # root_layer = self.getcurrentLayer()

        so.tab = so.tab.replace('"', '')  # removes de exceding double quotes from the string

        # latex related preamble
        self.preambleFile = os.getcwd() + '/logicGatesPreamble.tex'

        self.fontSize = 6.0
        self.fontSizeSmall = self.fontSize * 0.7
        self.textOffset = self.fontSize / 1.5  # offset between symbol and text
        self.textOffsetSmall = self.fontSizeSmall / 2  # offset between symbol and text
        self.textStyle = inkDraw.textStyle.setSimpleBlack(self.fontSize, justification='center')
        self.textStyleSmall = inkDraw.textStyle.setSimpleBlack(self.fontSizeSmall, justification='center')

        if so.symbolSize.lower() == 'large':
            self.totalHeight = 30  # total height of the logic gate
            self.totalWidth = 50  # total width of the logic gate, including in/output
            self.lengthTerm = 10  # length of the terminals
            self.lineWidthBody = 1.8
            self.NOTcircleRadius = 2

        if so.symbolSize.lower() == 'small':
            self.totalHeight = 20  # total height of the logic gate
            self.totalWidth = 40  # total width of the logic gate, including in/output
            self.lengthTerm = 10  # length of the terminals
            self.lineWidthBody = 1.4
            self.NOTcircleRadius = 1.5

        self.lineWidth = 1.0
        self.lineStyle = inkDraw.lineStyle.setSimpleBlack(self.lineWidth)
        self.lineStyleBody = inkDraw.lineStyle.setSimpleBlack(self.lineWidthBody)

        self.cleanDefs()

        # --------------------------
        # Gates
        # ---------------------------

        if so.tab == 'Gates':

            N_input = so.nInput
            inputVector = [True] * N_input

            # vector with type of inputs (regular or inverted)
            so.InputTypes = so.InputTypes.replace(' ', '').replace(',', '')
            for i in range(min(N_input, len(so.InputTypes))):
                if so.InputTypes[i] == '0':
                    inputVector[i] = False

            if so.ANDgate:
                self.createAND(root_layer, inputVector, True, position)
            if so.NANDgate:
                self.createAND(root_layer, inputVector, False, position)

            if so.ORgate:
                self.createOR(root_layer, inputVector, True, position)
            if so.NORgate:
                self.createOR(root_layer, inputVector, False, position)

            if so.XORgate:
                self.createXOR(root_layer, inputVector, True, position)
            if so.XNORgate:
                self.createXOR(root_layer, inputVector, False, position)

            if so.NOTgate:
                self.createNOT(root_layer, position, isBuffer=False)

            if so.BUFgate:
                self.createNOT(root_layer, position, isBuffer=True)
        # --------------------------
        # Latches and Flip-flops
        # ---------------------------

        if so.tab == 'Latches':
            if so.latchGateLogic == 'HIGH':
                logic = True
            else:
                logic = False
            self.createLatch(root_layer, position, type=so.latchType, controlGate=so.latchGate, controlGateLogic=logic,
                             asynPreset=int(so.latchPreset), asynClear=int(so.latchClear), size=so.latchSize, suppressq=so.latchSuppressq,
                             suppressNOTq=so.latchSuppressNOTq)

        # --------------------------
        # SignalsAndExpressions
        # ---------------------------
        if so.tab == 'SignalsAndExpressions':

            if so.subTab_sigExp == 'expressions':
                if not inkDraw.useLatex:
                    value = so.boolExpression.replace(' ', '').replace(r'\AND', '.').replace(r'\OR', '+').replace('\XOR', u'\u2295')
                    value = value.replace('\XNOR', u'\u2299').replace(r'\NOT', u'\u00AC').replace('{', '(').replace('}', ')')  # removes LaTeX stuff
                else:
                    value = '$' + so.boolExpression + '$'

                inkDraw.text.latex(self, root_layer, value, [position[0], position[1]], self.fontSize, refPoint='cc', preambleFile=self.preambleFile)

            if so.subTab_sigExp == 'signals':

                if so.signal == "GND":
                    self.drawGND(root_layer, position, angleDeg=so.signalRot)
                    return

                if so.signal == "common":
                    self.drawCommon(root_layer, position, angleDeg=so.signalRot)
                    return

                if so.signal in ["custom", "digital"]:
                    text = so.signalVal

                if so.signal == "digital":
                    self.drawDigital(root_layer, position, angleDeg=so.signalRot, nodalVal=text)
                    return

                if so.signal == "+vcc":
                    text = '+V_{cc}'

                if so.signal == "-vcc":
                    text = '-V_{cc}'

                if so.signal == "+5V":
                    text = r'+5\volt'

                if so.signal == "-5V":
                    text = r'-5\volt'

                if so.signal == "+15V":
                    text = r'+15\volt'

                if so.signal == "-15V":
                    text = r'-15\volt'

                if so.signal == "EN":
                    text = r'EN'

                if so.signal == "CLK":
                    text = r'CLK'

                if so.signal == "ENi":
                    text = r'\NOT{EN}'

                if so.signal == "CLKi":
                    text = r'\NOT{CLK}'

                self.drawV(root_layer, position, angleDeg=so.signalRot, nodalVal=text, drawLine=so.signalDrawLine)
                return

    def createSignal(self, flagTrue, parent, position=[0, 0], direction='E', extraLength=0.0, label='input', name=None, fontSizeFactor=1.0,
                     isClock=False):
        """ Creates signals to logic Gates (inputs or outputs)

        flagTrue: TRUE: regular input.  FALSE: NOT input
        parent: parent object
        position: position [x,y]
        direction: orientation of the signal. Values possible: 'N', 'S', 'W', 'E'
        extraLength: add extra lenght to the input line. default: 0.0
        label: label of the object (it can be repeated)
        name: Name of the signal. In ``None`` (default) no name is added
        fontSizeFactor: font scale factor. Default: 1.0
        isClock: input is clock type. Default: False
        """

        group = self.createGroup(parent, label)
        elem = self.createGroup(group, label)

        if flagTrue:
            inkDraw.line.relCoords(elem, [[-self.lengthTerm - extraLength, 0]], position, label, self.lineStyle)

        else:
            inkDraw.line.absCoords(elem, [[-(self.NOTcircleRadius*2+self.lineWidth/2+self.lineWidth*0.9), 0], [-self.lengthTerm - extraLength, 0]], position, label, self.lineStyle)
            inkDraw.circle.centerRadius(elem, [-self.NOTcircleRadius - self.lineWidth, 0], self.NOTcircleRadius, position, label,
                                        inkDraw.lineStyle.setSimpleBlack(self.lineWidthBody*0.7))

        if isClock:
            inkDraw.line.absCoords(elem, [[0, -4], [4, 0], [0, 4]], position, label, inkDraw.lineStyle.setSimpleBlack(0.9))

        if isClock:
            offsetText = self.textOffset * fontSizeFactor + 4
        else:
            offsetText = self.textOffset * fontSizeFactor

        if direction == 'N':
            self.rotateElement(elem, position, -90)  # y direction is inverted
            posText = [position[0], position[1] + offsetText]
            justif = 'tc'
        if direction == 'S':
            self.rotateElement(elem, position, 90)  # y direction is inverted
            posText = [position[0], position[1] - offsetText]
            justif = 'bc'
        if direction == 'E':
            self.rotateElement(elem, position, 180)  # y direction is inverted
            posText = [position[0] - offsetText, position[1]]
            justif = 'cr'
        if direction == 'W':
            posText = [position[0] + offsetText, position[1]]
            justif = 'cl'

        if name:
            inkDraw.text.latex(self, group, name, position=posText, fontSize=self.fontSize * fontSizeFactor, refPoint=justif,
                               preambleFile=self.preambleFile)

    # ---------------------------------------------
    def createInput(self, flagTrue, parent, position=[0, 0], extraLength=0.0, label='input', name=None, fontSizeFactor=1.0):
        """ Creates input to logic Gates

        flagTrue: TRUE: regular input.  FALSE: NOT input
        parent: parent object
        position: position [x,y]
        extraLength: add extra lenght to the input line. default: 0.0
        label: label of the object (it can be repeated)
        name: Name of the signal. In ``None`` (default) no name is added
        fontSizeFactor: font scale factor. Default: 1.0
        """
        direction = 'W'
        self.createSignal(flagTrue, parent, position, direction, extraLength, label, name, fontSizeFactor)

    # ---------------------------------------------
    def createOutput(self, flagTrue, parent, position=[0, 0], extraLength=0.0, label='output', name=None, fontSizeFactor=1.0):
        """ Creates output to logic Gates

        flagTrue: TRUE: regular input.  FALSE: NOT input
        parent: parent object
        position: position [x,y]
        extraLength: add extra lenght to the input line. default: 0.0
        label: label of the object (it can be repeated)
        name: Name of the signal. In ``None`` (default) no name is added
        fontSizeFactor: font scale factor. Default: 1.0
        """
        direction = 'E'
        if flagTrue:
            self.createSignal(flagTrue, parent, [position[0], position[1]], direction, extraLength, label, name, fontSizeFactor)
        else:
            self.createSignal(flagTrue, parent, [position[0] - 0.5, position[1]], direction, extraLength + 0.5, label, name, fontSizeFactor)

    # ---------------------------------------------
    def drawANDBody(self, parent, position=[0, 0], label='BodyAND'):
        """ Creates body of AND logic Gate

        parent: parent object
        position: position [x,y]
        label: label of the object (it can be repeated)
        """

        h = self.totalHeight / 2.0  # half height
        R = h  # radius
        widthBase = self.totalWidth - 2 * self.lengthTerm - R  # length of the straight part of AND body

        group = self.createGroup(parent, label)

        inkDraw.line.absCoords(group, [[0, h], [-widthBase, h], [-widthBase, -h], [0, -h]], position, label, self.lineStyleBody)
        inkDraw.arc.centerAngStartAngEnd(group, [0, 0], R, 90, -90, position, label, self.lineStyleBody, largeArc=True)

    # ---------------------------------------------
    def drawORBody(self, parent, position=[0, 0], label='BodyOR'):
        """ Creates body of OR logic Gate

        parent: parent object
        position: position [x,y]
        label: label of the object (it can be repeated)
        """
        h = self.totalHeight / 2.0  # half height
        x = h + 5  # x distance of the tip to the center
        R = math.sqrt(((x * x - h * h) / (2 * h)) ** 2 + x * x)
        widthBase = self.totalWidth - 1.5 * self.lengthTerm - x  # length of the straight part of OR body

        group = self.createGroup(parent, label)

        inkDraw.line.absCoords(group, [[0, h], [-widthBase, h]], position, label, self.lineStyleBody)
        inkDraw.line.absCoords(group, [[0, -h], [-widthBase, -h]], position, label, self.lineStyleBody)
        inkDraw.arc.startEndRadius(group, [x, 0], [0, h], R, position, label, self.lineStyleBody, flagRightOf=False)
        inkDraw.arc.startEndRadius(group, [0, -h], [x, 0], R, position, label, self.lineStyleBody, flagRightOf=False)
        inkDraw.arc.startEndRadius(group, [-widthBase, -h], [-widthBase, h], self.totalHeight, position, label, self.lineStyleBody, flagRightOf=False)

        # ---------------------------------------------

    def drawXORBody(self, parent, position=[0, 0], label='BodyXOR'):
        """ Creates body of XOR logic Gate

        parent: parent object
        position: position [x,y]
        label: label of the object (it can be repeated)
        """
        h = self.totalHeight / 2.0  # half height
        x = h + 5  # x distance of the tip to the center
        R = math.sqrt(((x * x - h * h) / (2 * h)) ** 2 + x * x)
        space = 2.2*self.lineWidthBody  # space between parallel arcs
        widthBase = self.totalWidth - 1.5 * self.lengthTerm - x - space  # length of the straight part of AND body

        group = self.createGroup(parent, label)

        inkDraw.line.absCoords(group, [[0, h], [-widthBase, h]], position, label, self.lineStyleBody)
        inkDraw.line.absCoords(group, [[0, -h], [-widthBase, -h]], position, label, self.lineStyleBody)
        inkDraw.arc.startEndRadius(group, [x, 0], [0, h], R, position, label, self.lineStyleBody, flagRightOf=False)
        inkDraw.arc.startEndRadius(group, [0, -h], [x, 0], R, position, label, self.lineStyleBody, flagRightOf=False)
        inkDraw.arc.startEndRadius(group, [-widthBase, -h], [-widthBase, h], self.totalHeight, position, label, self.lineStyleBody, flagRightOf=False)
        inkDraw.arc.startEndRadius(group, [-widthBase - space, -h], [-widthBase - space, h], self.totalHeight, position, label, self.lineStyleBody,
                                   flagRightOf=False)

    # ---------------------------------------------
    def drawInputOR(self, parent, vectorInput=[True, True], position=[0, 0], label='InputORGate'):
        """ Creates inputs to OR/NOR/XOR/XNOR logic Gates

        parent: parent object
        vectorInput: vector with booleans. Default [True,True]
                    It's length is the number of inputs of the gate.
                    For each input (top to bottom) True: regular input  False: Negated input.
        position: position [x,y]
        label: label of the object (it can be repeated)
        """

        group = self.createGroup(parent, label)

        inputSpace = (2/3)*self.totalHeight
        N_input = len(vectorInput)
        spaceBetweenInputs = inputSpace / (N_input - 1)
        r = self.totalHeight  # radius
        H = self.totalHeight / 2.0  # total height
        h_max = inputSpace/2  # maximum height of inputs

        for i in range(0, N_input):
            h = -(h_max - i * spaceBetweenInputs)  # bottom to up because inkscape is upside down =(
            x = math.sqrt(r ** 2 - h ** 2)
            L0 = math.sqrt(r ** 2 - H ** 2)
            L = x - L0

            self.createInput(vectorInput[i], group, [L + position[0], h + position[1]], L - 2.5,
                             'input' + str(i))  # 2.5 for reducing a little the lengh so that AND and OR gates have the same width

    # ---------------------------------------------
    def drawInputAND(self, parent, vectorInput=[True, True], position=[0, 0], label='InputANDGate'):
        """ Creates inputs to AND,NAND logic Gates

        parent: parent object
        vectorInput: vector with booleans. Default [True,True]
                    It's length is the number of inputs of the gate.
                    For each input (top to bottom) True: regular input  False: Negated input.
        position: position [x,y]
        label: label of the object (it can be repeated)
        """

        group = self.createGroup(parent, label)

        inputSpace = (2/3)*self.totalHeight
        N_input = len(vectorInput)
        spaceBetweenInputs = inputSpace / (N_input - 1)
        h_max = inputSpace/2  # maximum height of inputs

        for i in range(0, N_input):
            h = -(h_max - i * spaceBetweenInputs)
            self.createInput(vectorInput[i], group, [position[0], h + position[1]], 0, 'input' + str(i))

    # ---------------------------------------------
    def createAND(self, parent, vectorInput=[True, True], output=True, position=[0, 0], label='BodyAND'):
        """ Creates AND/NAND logic Gate

        parent: parent object
        vectorInput: vector with booleans. Default [True,True]
                    It's length is the number of inputs of the gate.
                    For each input (top to bottom) True: regular input  False: Negated input.
        output: selects AND or NAND gate  (Default True)
                  True: AND
                  False: NAND
        position: position [x,y]
        label: label of the object (it can be repeated)
        """
        h = self.totalHeight / 2.0  # half height
        R = h  # radius
        widthBase = self.totalWidth - 2 * self.lengthTerm - R  # length of the straight part of AND body

        group = self.createGroup(parent, label)
        x_output = R  # x coordinate of the output

        self.drawANDBody(group, position)
        self.drawInputAND(group, vectorInput, [-widthBase + position[0], position[1]])
        self.createOutput(output, group, [x_output + position[0], position[1]])

    # ---------------------------------------------
    def createOR(self, parent, vectorInput=[True, True], output=True, position=[0, 0], label='ORGate'):
        """ Creates OR/NOR logic Gate

        parent: parent object
        vectorInput: vector with booleans. Default [True,True]
                    It's length is the number of inputs of the gate.
                    For each input (top to bottom) True: regular input  False: Negated input.
        output: selects OR or NOR gate  (Default True)
                  True: OR
                  False: NOR
        position: position [x,y]
        label: label of the object (it can be repeated)
        """

        h = self.totalHeight / 2.0  # half height
        x = h + 5  # x distance of the tip to the center
        R = math.sqrt(((x * x - h * h) / (2 * h)) ** 2 + x * x)
        widthBase = self.totalWidth - 1.5 * self.lengthTerm - x  # length of the straight part of OR body

        group = self.createGroup(parent, label)
        x_output = self.totalHeight / 2.0 + 5  # x coordinate of the output

        self.drawORBody(group, position)
        self.drawInputOR(group, vectorInput, [position[0] - widthBase, position[1]])
        self.createOutput(output, group, [x_output + position[0], position[1]], -2.5)  # 2.5 for reducing a little the lengh so that AND and

    # ---------------------------------------------
    def createXOR(self, parent, vectorInput=[True, True], output=True, position=[0, 0], label='XORGate'):
        """ Creates XOR/XNOR logic Gate

        parent: parent object
        vectorInput: vector with booleans. Default [True,True]
                    It's length is the number of inputs of the gate.
                    For each input (top to bottom) True: regular input  False: Negated input.
        output: selects OR or NOR gate  (Default True)
                  True: XOR
                  False: XNOR
        position: position [x,y]
        label: label of the object (it can be repeated)
        """

        h = self.totalHeight / 2.0  # half height
        x = h + 5  # x distance of the tip to the center
        R = math.sqrt(((x * x - h * h) / (2 * h)) ** 2 + x * x)
        space = 2.2*self.lineWidthBody  # space between parallel arcs
        widthBase = self.totalWidth - 1.5 * self.lengthTerm - x  # length of the straight part of AND body

        group = self.createGroup(parent, label)
        x_output = self.totalHeight / 2.0 + 5  # x coordinate of the output

        self.drawXORBody(group, position)
        self.drawInputOR(group, vectorInput, [position[0] - widthBase, position[1]])
        self.createOutput(output, group, [x_output + position[0], position[1]], -2.5)  # 2.5 for reducing a little the lengh so that AND and

        # ---------------------------------------------

    def createNOT(self, parent, position=[0, 0], label='NOTGate', isBuffer=False):
        """ Creates NOT logic Gate

        parent: parent object
        vectorInput: vector with booleans. Default [True,True]
                    It's length is the number of inputs of the gate.
                    For each input (top to bottom) True: regular input  False: Negated input.
        position: position [x,y]
        label: label of the object (it can be repeated)
        isBuffer: if False, create a NOT gate, if True, create a buffer gate
        """

        triangleSide = 2/3*self.totalHeight
        triangle_height = triangleSide * math.sqrt(3) / 2

        group = self.createGroup(parent, label)
        inkDraw.line.absCoords(group, [[0, triangleSide / 2], [triangle_height, 0], [0, -triangleSide / 2], [0, triangleSide / 2]], position, 'not1',
                               self.lineStyleBody, True)

        self.createInput([True], group, position)
        self.createOutput(isBuffer, group, [triangle_height + 0.5 + position[0], 0 + position[1]], (self.totalWidth - 2*self.lengthTerm) - triangle_height - self.lengthTerm - 0.5)

        # ---------------------------------------------

    def drawV(self, parent, position=[0, 0], label='GND', angleDeg=0, nodalVal='V_{cc}', drawLine=True):
        """ draws a Voltage node

        parent: parent object
        position: position [x,y]
        label: label of the object (it can be repeated)
        angleDeg: rotation angle in degrees counter-clockwise (default 0)
        nodalVal: name of the node (default: 'V_{cc}')
        drawLine: draws line for connection (default: True)
        """
        linestyleBlackFill = inkDraw.lineStyle.set(lineWidth=0.7, fillColor=inkDraw.color.defined('black'))
        group = self.createGroup(parent, label)
        elem = self.createGroup(group, label)

        inkDraw.circle.centerRadius(elem, position, 1.0, offset=[0, 0], lineStyle=linestyleBlackFill)
        if drawLine:
            inkDraw.line.relCoords(elem, [[0, 10]], position)

        # text
        if abs(angleDeg) <= 90:
            justif = 'bc'
            pos_text = [position[0], position[1] - self.textOffset]
        else:
            justif = 'tc'
            pos_text = [position[0], position[1] + self.textOffset]

        if not inkDraw.useLatex:
            value = nodalVal.replace('_', '').replace(r'\NOT', u'\u00AC').replace('{', '').replace('}', '').replace(r'\volt',
                                                                                                                    'V')  # removes LaTeX stuff
        else:
            value = '$' + nodalVal + '$'
        temp = inkDraw.text.latex(self, group, value, pos_text, fontSize=self.fontSize, refPoint=justif, preambleFile=self.preambleFile)

        self.rotateElement(temp, position, -angleDeg)

        if angleDeg != 0:
            self.rotateElement(group, position, angleDeg)

        return group

    # ---------------------------------------------
    def drawGND(self, parent, position=[0, 0], label='GND', angleDeg=0):
        """ draws a GND

        parent: parent object
        position: position [x,y]
        label: label of the object (it can be repeated)
        angleDeg: rotation angle in degrees counter-clockwise (default 0)
        """

        group = self.createGroup(parent, label)
        elem = self.createGroup(group, label)

        inkDraw.line.relCoords(elem, [[0, 10]], position)
        inkDraw.line.relCoords(elem, [[-14, 0]], [position[0] + 7, position[1] + 10])
        inkDraw.line.relCoords(elem, [[-7, 0]], [position[0] + 3.5, position[1] + 12])
        inkDraw.line.relCoords(elem, [[-2, 0]], [position[0] + 1, position[1] + 14])

        if angleDeg != 0:
            self.rotateElement(group, position, angleDeg)

        return group

    # ---------------------------------------------
    def drawDigital(self, parent, position=[0, 0], label='GPIO', angleDeg=0, nodalVal='GPIO'):
        """ draws a digital signal

        parent: parent object
        position: position [x,y]
        label: label of the object (it can be repeated)
        angleDeg: rotation angle in degrees counter-clockwise (default 0)
        nodalVal: name of the node (default: 'V_{cc}')
        """
        linestyleBlackFill = inkDraw.lineStyle.set(lineWidth=0.8)
        group = self.createGroup(parent, label)
        elem = self.createGroup(group, label)

        inkDraw.line.relCoords(elem, [[0, 4], [25, 0], [4, -4], [-4, -4], [-25, 0], [0, 4]], [position[0], position[1]], lineStyle=linestyleBlackFill)

        # text
        if not inkDraw.useLatex:
            value = nodalVal.replace('_', '').replace('{', '').replace('}', '').replace(r'\volt', 'V')  # removes LaTeX stuff
        else:
            value = '$' + nodalVal + '$'
        temp = inkDraw.text.latex(self, group, value, [position[0] + 2, position[1]], fontSize=self.fontSize, refPoint='cl',
                                  preambleFile=self.preambleFile)

        self.rotateElement(temp, position, -angleDeg)

        if angleDeg != 0:
            self.rotateElement(group, position, angleDeg)

        return group;

    def drawCommon(self, parent, position=[0, 0], label='Common', angleDeg=0):
        """ draws a GND

        parent: parent object
        position: position [x,y]
        label: label of the object (it can be repeated)
        angleDeg: rotation angle in degrees counter-clockwise (default 0)
        """

        group = self.createGroup(parent, label)
        elem = self.createGroup(group, label)

        inkDraw.line.relCoords(elem, [[0, 10]], position)
        inkDraw.line.relCoords(elem, [[-10, 0], [5, 5], [5, -5]], [position[0] + 5, position[1] + 10])

        if angleDeg != 0:
            self.rotateElement(group, position, angleDeg)

        return group

    # ---------------------------------------------
    def createLatch(self, parent, position=[0, 0], label='Latch', type='SRnor', controlGate='none', controlGateLogic=True, asynPreset=0, asynClear=0,
                    size='large', suppressq=False, suppressNOTq=False):
        """ draws latches

        parent: parent object
        position: position [x,y]
        label: label of the object (it can be repeated)
        type: type of latch/Flip-flop. Available values: 'SRnor','SRnand','D','JK','T'
        controlGate: type of the gate input: available values: 'none','level', 'edge'
        controlGateLogic: True: activate HIGH (or rising edge)  False: activate LOW (or falling edge)
        asynPreset: Asyncrhonous preset
        asynClear: Asyncrhonous clear
            1: active HIGH
            0: no input
            -1: active LOW
        size: predefined size. Available values: 'large', 'medium', 'small'
        suppressq: suppress drawing he direct state output. Default: False
        suppressNOTq: suppress drawing he inverted state output. Default: False
        """
        group = self.createGroup(parent, label)

        if type == 'SRnor' or type == 'SRnand' or type == 'JK':
            if size == 'large':
                w = 50
                h = 70
                dist_signal = 20
                y_controlGate = 0
            if size == 'medium':
                w = 40
                h = 50
                dist_signal = 15
                y_controlGate = 0
            if size == 'small':
                w = 30
                h = 40
                dist_signal = 10
                y_controlGate = 0

        if type == 'D' or type == 'T':
            if size == 'large':
                w = 50
                h = 60
                dist_signal = 15
                y_controlGate = 15
            if size == 'medium':
                w = 40
                h = 40
                dist_signal = 10
                y_controlGate = 10
            if size == 'small':
                w = 30
                h = 35
                dist_signal = 7.5
                y_controlGate = 7.5

        if size == 'large':
            fontSizeFactorG = 1.2
            fontSizeFactorS = 0.8
        if size == 'medium':
            fontSizeFactorG = 1.0
            fontSizeFactorS = 0.6
        if size == 'small':
            fontSizeFactorG = 0.7
            fontSizeFactorS = 0.5

        x_min = position[0] - w / 2.0
        x_max = position[0] + w / 2.0
        y_min = position[1] + h / 2.0
        y_max = position[1] - h / 2.0

        inkDraw.rectangle.widthHeightCenter(group, centerPoint=position, width=w, height=h, lineStyle=inkDraw.lineStyle.setSimpleBlack(1.5))

        if not suppressq:
            if not inkDraw.useLatex:
                self.createOutput(True, group, position=[x_max, position[1] - dist_signal], extraLength=0.0, label='Q', name='Q',
                                  fontSizeFactor=fontSizeFactorG)
            else:
                self.createOutput(True, group, position=[x_max, position[1] - dist_signal], extraLength=0.0, label='Q', name='$Q$',
                                  fontSizeFactor=fontSizeFactorG)

        if not suppressNOTq:
            if not inkDraw.useLatex:
                self.createOutput(True, group, position=[x_max, position[1] + dist_signal], extraLength=0.0, label='notQ', name=u'\u00ACQ',
                                  fontSizeFactor=fontSizeFactorG)
            else:
                self.createOutput(True, group, position=[x_max, position[1] + dist_signal], extraLength=0.0, label='notQ', name=r'$\NOT{Q}$',
                                  fontSizeFactor=fontSizeFactorG)

                # Asyncronous Preset and Clear
        if asynPreset == 1:
            self.createSignal(True, group, position=[position[0], y_max], direction='N', name='PRE', fontSizeFactor=fontSizeFactorS)
        elif asynPreset == -1:
            self.createSignal(False, group, position=[position[0], y_max], direction='N', name='PRE', fontSizeFactor=fontSizeFactorS)

        if asynClear == 1:
            self.createSignal(True, group, position=[position[0], y_min], direction='S', name='CLR', fontSizeFactor=fontSizeFactorS)
        elif asynClear == -1:
            self.createSignal(False, group, position=[position[0], y_min], direction='S', name='CLR', fontSizeFactor=fontSizeFactorS)

        if controlGate == 'level':
            self.createSignal(controlGateLogic, group, position=[x_min, position[1] + y_controlGate], direction='W', name='EN', isClock=False,
                              fontSizeFactor=fontSizeFactorS)
        if controlGate == 'edge':
            self.createSignal(controlGateLogic, group, position=[x_min, position[1] + y_controlGate], direction='W', name='CLK', isClock=True,
                              fontSizeFactor=fontSizeFactorS)

        if type == 'SRnor' or type == 'JK':
            if not inkDraw.useLatex:
                self.createInput(True, group, position=[x_min, position[1] - dist_signal], extraLength=0.0, name=type[0],
                                 fontSizeFactor=fontSizeFactorG)
                self.createInput(True, group, position=[x_min, position[1] + dist_signal], extraLength=0.0, name=type[1],
                                 fontSizeFactor=fontSizeFactorG)
            else:
                self.createInput(True, group, position=[x_min, position[1] - dist_signal], extraLength=0.0, name='$' + type[0] + '$',
                                 fontSizeFactor=fontSizeFactorG)
                self.createInput(True, group, position=[x_min, position[1] + dist_signal], extraLength=0.0, name='$' + type[1] + '$',
                                 fontSizeFactor=fontSizeFactorG)

        elif type == 'SRnand':
            if not inkDraw.useLatex:
                input1 = u'\u00AC%s' % type[0]
                input2 = u'\u00AC%s' % type[1]
            else:
                input1 = r'\NOT{%s}' % type[0]
                input2 = r'\NOT{%s}' % type[1]
            self.createInput(True, group, position=[x_min, position[1] - dist_signal], extraLength=0.0, name=input1, fontSizeFactor=fontSizeFactorG)
            self.createInput(True, group, position=[x_min, position[1] + dist_signal], extraLength=0.0, name=input2, fontSizeFactor=fontSizeFactorG)
        elif type == 'D' or type == 'T':
            if not inkDraw.useLatex:
                self.createInput(True, group, position=[x_min, position[1] - dist_signal], extraLength=0.0, name=type, fontSizeFactor=fontSizeFactorG)
            else:
                self.createInput(True, group, position=[x_min, position[1] - dist_signal], extraLength=0.0, name='$' + type + '$',
                                 fontSizeFactor=fontSizeFactorG)


if __name__ == '__main__':
    logic = LogicGates()

    debugMode = False

    if debugMode:
        tempFile = '/home/fernando/lixo_defs.svg'

        logic.run([r'--ANDgate=True', tempFile], output=os.devnull)
        logic.document.write('/home/fernando/temp_debug_out.svg')

    else:
        logic.run()
