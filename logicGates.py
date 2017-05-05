#!/usr/bin/python

import inkex
import inkscapeMadeEasy_Base as inkBase
import inkscapeMadeEasy_Draw as inkDraw
import inkscapeMadeEasy_Plot as inkPlot
import math
import os
import re
#---------------------------------------------
class LogicGates(inkBase.inkscapeMadeEasy):
  def __init__(self):
    inkex.Effect.__init__(self)

    self.OptionParser.add_option("--tab",action="store", type="string",dest="tab", default="object") 
    
    self.OptionParser.add_option("--ANDgate", action="store", type="inkbool", dest="ANDgate", default=False)
    self.OptionParser.add_option("--ORgate", action="store", type="inkbool", dest="ORgate", default=False)
    self.OptionParser.add_option("--XORgate", action="store", type="inkbool", dest="XORgate", default=False)
    self.OptionParser.add_option("--NOTgate", action="store", type="inkbool", dest="NOTgate", default=False)
    self.OptionParser.add_option("--NANDgate", action="store", type="inkbool", dest="NANDgate", default=False)
    self.OptionParser.add_option("--NORgate", action="store", type="inkbool", dest="NORgate", default=False)
    self.OptionParser.add_option("--XNORgate", action="store", type="inkbool", dest="XNORgate", default=False)
        
    self.OptionParser.add_option("--nInput",action="store", type="int",dest="nInput", default=2)
    self.OptionParser.add_option("--InputTypes", action="store", type="string", dest="InputTypes", default='11')

    self.OptionParser.add_option("--latchType",action="store", type="string",dest="latchType", default='none')
    self.OptionParser.add_option("--latchGate",action="store", type="string",dest="latchGate", default='none')
    self.OptionParser.add_option("--latchGateLogic",action="store", type="string",dest="latchGateLogic", default='HIGH')
    self.OptionParser.add_option("--latchPreset",action="store", type="string",dest="latchPreset", default='0')
    self.OptionParser.add_option("--latchClear",action="store", type="string",dest="latchClear", default='0')

    self.OptionParser.add_option("--flagSignal", action="store", type="inkbool", dest="flagSignal", default=False)
    self.OptionParser.add_option("--signal",action="store", type="string",dest="signal", default='GND')
    self.OptionParser.add_option("--signalVal", action="store", type="string", dest="signalVal", default='E') 
    self.OptionParser.add_option("--signalRot", action="store", type="float", dest="signalRot", default=0)
    self.OptionParser.add_option("--signalDrawLine", action="store", type="inkbool", dest="signalDrawLine", default=True)
    
    self.OptionParser.add_option("--flagExpression", action="store", type="inkbool", dest="flagExpression", default=False)
    self.OptionParser.add_option("--boolExpression", action="store", type="string", dest="boolExpression", default='')
    self.OptionParser.add_option("--fontSize", action="store", type="float", dest="fontSize", default=5.0)

    self.lineStyle=inkDraw.lineStyle.setSimpleBlack()
    self.lineStyleBody=inkDraw.lineStyle.setSimpleBlack(1.8)
    self.totalHeight=30  # total height of the logic gate
    self.totalWidth=50    # total width of the logic gate, including in/output
    self.lengthTerm=10  # length of the terminals
    
  def effect(self):
    
    so = self.options
    
    # sets the position to the viewport center, round to next 10.
    position=[self.view_center[0],self.view_center[1]]
    position[0]=int(math.ceil(position[0] / 10.0)) * 10
    position[1]=int(math.ceil(position[1] / 10.0)) * 10

    #root_layer = self.current_layer
    root_layer = self.document.getroot()
    
    so.tab = so.tab.replace('"','')   # removes de exceding double quotes from the string
    
    #latex related preamble
    self.preambleFile=os.getcwd() + '/textextLib/CircuitSymbolsLatexPreamble.tex'

    self.fontSize=float(so.fontSize)
    self.fontSizeSmall=self.fontSize*0.7
    self.textOffset = self.fontSize/1.5  # offset between symbol and text
    self.textOffsetSmall = self.fontSizeSmall/2  # offset between symbol and text
    self.textStyle = inkDraw.textStyle.setSimpleBlack(self.fontSize,justification='center')
    self.textStyleSmall = inkDraw.textStyle.setSimpleBlack(self.fontSizeSmall,justification='center')

    # --------------------------
    # Gates
    #---------------------------
    
    if so.tab=='Gates':
      
      N_input=so.nInput
      inputVector=[True] * N_input
      
      # vector with type of inputs (regular or inverted)
      so.InputTypes=so.InputTypes.replace(' ','').replace(',','')
      for i in range(min(N_input,len(so.InputTypes))):
        if so.InputTypes[i]=='0':
          inputVector[i]=False

      if so.ANDgate:
        self.createAND(root_layer,inputVector,True,position)
      if so.NANDgate:
        self.createAND(root_layer,inputVector,False,position)
      
      if so.ORgate:
        self.createOR(root_layer,inputVector,True,position)
      if so.NORgate:
        self.createOR(root_layer,inputVector,False,position)
      
      if so.XORgate:
        self.createXOR(root_layer,inputVector,True,position)
      if so.XNORgate:
        self.createXOR(root_layer,inputVector,False,position)
        
      if so.NOTgate:
        self.createNOT(root_layer,position)
        
    # --------------------------
    # Latches and Flip-flops
    #---------------------------
    
    if so.tab=='Latches':
      if so.latchGateLogic=='HIGH':
        logic=True
      else:
        logic=False
      self.createLatch(root_layer,position,type=so.latchType,controlGate=so.latchGate,controlGateLogic=logic,asynPreset=int(so.latchPreset),asynClear=int(so.latchClear))

    # --------------------------
    # SignalsAndExpressions
    #---------------------------
    if so.tab=='SignalsAndExpressions':
      
      if so.flagExpression:
        if not inkDraw.useLatex:
          value = so.boolExpression.replace(' ','').replace(r'\AND','.').replace(r'\OR','+').replace('\XOR',u'\u2295') \
                   .replace('\XNOR',u'\u2299').replace(r'\NOT',u'\u00AC').replace('{','(').replace('}',')')  # removes LaTeX stuff
        else:
          value = '$'+so.boolExpression+'$'
          
        inkDraw.text.latex(self,root_layer,value,[position[0],position[1]+self.totalHeight], self.fontSize,refPoint='cc',preambleFile=self.preambleFile)

      if so.flagSignal:
          
        if so.signal=="GND":
          self.drawGND(root_layer,position,angleDeg=so.signalRot)
          return
          
        if so.signal=="common":
          self.drawCommon(root_layer,position,angleDeg=so.signalRot)
          return
          
        if so.signal=="custom":
          text=so.signalVal
          
        if so.signal=="+vcc":
          text='+V_{cc}'
          
        if so.signal=="-vcc":
          text='-V_{cc}'
          
        if so.signal=="+5V":
          text=r'+5\volt'
          
        if so.signal=="-5V":
          text=r'-5\volt'
          
        if so.signal=="+15V":
          text=r'+15\volt'
          
        if so.signal=="-15V":
          text=r'-15\volt'
        
        self.drawV(root_layer,position,angleDeg=so.signalRot,nodalVal=text,drawLine=so.signalDrawLine)
        return
      
  def createSignal(self,flagTrue,parent,position=[0, 0],direction='E',extraLength=0.0,label='input',name=None,fontSizeFactor=1.0,isClock=False):
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
    
    group = self.createGroup(parent,label)
    elem = self.createGroup(group,label)
    
    if flagTrue:
      inkDraw.line.relCoords( elem,[[-self.lengthTerm-extraLength, 0]], position,label, self.lineStyle)
      
    else:
      inkDraw.line.absCoords(elem, [[-5.5, 0],[-self.lengthTerm-extraLength,0]], position,label, self.lineStyle)
      inkDraw.circle.centerRadius(elem, [-3,0], 2, position,label, inkDraw.lineStyle.setSimpleBlack(1.2))
    
    if isClock:
      inkDraw.line.absCoords( elem,[[0, -4],[4,0],[0,4]], position,label, inkDraw.lineStyle.setSimpleBlack(0.9))

    if isClock:
      offsetText=self.textOffsetSmall*fontSizeFactor+4
    else:
      offsetText=self.textOffsetSmall*fontSizeFactor
    
    
    if direction=='N':
      self.rotateElement(elem,position,-90)  # y direction is inverted
      posText=[position[0],position[1]+offsetText]
      justif='tc'
    if direction=='S':
      self.rotateElement(elem,position,90)  # y direction is inverted
      posText=[position[0],position[1]-offsetText]
      justif='bc'
    if direction=='E':
      self.rotateElement(elem,position,180)  # y direction is inverted
      posText=[position[0]-offsetText,position[1]]
      justif='cr'
    if direction=='W':
      posText=[position[0]+offsetText,position[1]]
      justif='cl'
      
    if name:
      inkDraw.text.latex(self,group,name,position=posText,fontSize=self.fontSizeSmall*fontSizeFactor,refPoint=justif,preambleFile=self.preambleFile)
    
  #---------------------------------------------
  def createInput(self,flagTrue,parent,position=[0, 0],extraLength=0.0,label='input',name=None,fontSizeFactor=1.0):
    """ Creates input to logic Gates
    
    flagTrue: TRUE: regular input.  FALSE: NOT input
    parent: parent object
    position: position [x,y]
    extraLength: add extra lenght to the input line. default: 0.0
    label: label of the object (it can be repeated)
    name: Name of the signal. In ``None`` (default) no name is added
    fontSizeFactor: font scale factor. Default: 1.0
    """
    direction='W'
    self.createSignal(flagTrue,parent,position,direction,extraLength,label,name,fontSizeFactor)
    
     
  #---------------------------------------------
  def createOutput(self,flagTrue,parent,position=[0, 0],extraLength=0.0,label='output',name=None,fontSizeFactor=1.0):
    """ Creates output to logic Gates
    
    flagTrue: TRUE: regular input.  FALSE: NOT input
    parent: parent object
    position: position [x,y]
    extraLength: add extra lenght to the input line. default: 0.0
    label: label of the object (it can be repeated)
    name: Name of the signal. In ``None`` (default) no name is added
    fontSizeFactor: font scale factor. Default: 1.0
    """
    direction='E'
    if flagTrue:
      self.createSignal(flagTrue,parent,[position[0],position[1]],direction,extraLength,label,name,fontSizeFactor)
    else:
      self.createSignal(flagTrue,parent,[position[0]-0.5,position[1]],direction,extraLength+0.5,label,name,fontSizeFactor)
      
  #---------------------------------------------
  def drawANDBody(self,parent,position=[0, 0],label='BodyAND'):
    """ Creates body of AND logic Gate
    
    parent: parent object
    position: position [x,y]
    label: label of the object (it can be repeated)
    """
    
    h=self.totalHeight/2.0 # half height
    R=h  # radius
    widthBase=self.totalWidth-2*self.lengthTerm-R # length of the straight part of AND body
    
    group = self.createGroup(parent,label)
  
    inkDraw.line.absCoords(group, [[0, -h],[-widthBase,-h],[-widthBase,h]], position,label, self.lineStyleBody)
    inkDraw.line.absCoords(group, [[-widthBase,h],[0,h]], position,label, self.lineStyleBody)
    inkDraw.arc.centerAngStartAngEnd(group, [0,0], R, 90, -90, position,label, self.lineStyleBody,largeArc=True)
        
  #---------------------------------------------
  def drawORBody(self,parent,position=[0, 0],label='BodyOR'):
    """ Creates body of OR logic Gate
    
    parent: parent object
    position: position [x,y]
    label: label of the object (it can be repeated)
    """
    h=self.totalHeight/2.0 # half height
    x=h+5 # x distance of the tip to the center
    R=math.sqrt( ( (x*x-h*h)/(2*h) )**2 + x*x )
    widthBase=self.totalWidth-2*self.lengthTerm-15 # length of the straight part of AND body    
    
    group = self.createGroup(parent,label)
    
    inkDraw.line.absCoords(group, [[0,h],[-widthBase,h]], position,label, self.lineStyleBody)
    inkDraw.line.absCoords(group, [[0,-h],[-widthBase,-h]], position,label, self.lineStyleBody)
    inkDraw.arc.startEndRadius(group,[x,0], [0,h], R, position,label, self.lineStyleBody,flagRightOf=False,flagOpen=True)
    inkDraw.arc.startEndRadius(group,[0,-h], [x,0],R, position,label, self.lineStyleBody,flagRightOf=False,flagOpen=True)
    inkDraw.arc.startEndRadius(group,[-widthBase,-h], [-widthBase,h], self.totalHeight, position,label, self.lineStyleBody,flagRightOf=False,flagOpen=True)

    #---------------------------------------------
  def drawXORBody(self,parent,position=[0, 0],label='BodyXOR'):
    """ Creates body of XOR logic Gate
    
    parent: parent object
    position: position [x,y]
    label: label of the object (it can be repeated)
    """
    h=self.totalHeight/2.0 # half height
    x=h+5 # x distance of the tip to the center
    R=math.sqrt( ( (x*x-h*h)/(2*h) )**2 + x*x )
    space = 4 # space between parallel arcs
    widthBase=self.totalWidth-2*self.lengthTerm-15-space # length of the straight part of AND body   
    
    group = self.createGroup(parent,label)
    
    inkDraw.line.absCoords(group, [[0,h],[-widthBase,h]], position,label, self.lineStyleBody)
    inkDraw.line.absCoords(group, [[0,-h],[-widthBase,-h]], position,label,  self.lineStyleBody)
    inkDraw.arc.startEndRadius(group, [x,0], [0,h], R, position,label, self.lineStyleBody,flagRightOf=False,flagOpen=True)
    inkDraw.arc.startEndRadius(group, [0,-h], [x,0],R, position,label, self.lineStyleBody,flagRightOf=False,flagOpen=True)
    inkDraw.arc.startEndRadius(group, [-widthBase,-h], [-widthBase,h], self.totalHeight, position,label, self.lineStyleBody,flagRightOf=False,flagOpen=True)
    inkDraw.arc.startEndRadius(group, [-widthBase-space,-h], [-widthBase-space,h], self.totalHeight, position,label, self.lineStyleBody,flagRightOf=False,flagOpen=True)
    
  #---------------------------------------------
  def drawInputOR(self,parent,vectorInput=[True, True],position=[0, 0],label='InputORGate'):
    """ Creates inputs to OR/NOR/XOR/XNOR logic Gates
    
    parent: parent object
    vectorInput: vector with booleans. Default [True,True]
                It's length is the number of inputs of the gate. 
                For each input (top to bottom) True: regular input  False: Negated input.
    position: position [x,y]
    label: label of the object (it can be repeated)
    """

    group = self.createGroup(parent,label)
        
    N_input=len(vectorInput)
    spaceBetweenInputs=20.0/(N_input-1)
    r=self.totalHeight  # radius
    H=self.totalHeight/2.0  # total height
    h_max=10 # maximum height of inputs
    
    for i in range(0, N_input):
      h=-(h_max-i*spaceBetweenInputs)  # bottom to up because inkscape is upside down =(
      x=math.sqrt(r**2-h**2)
      L0=math.sqrt(r**2-H**2)
      L=x-L0
      
      self.createInput(vectorInput[i],group,[L+position[0], h+position[1]],L-2.5,'input' + str(i))# 2.5 for reducing a little the lengh so that AND and OR gates have the same width
      
  #---------------------------------------------
  def drawInputAND(self,parent,vectorInput=[True, True],position=[0, 0],label='InputANDGate'):
    """ Creates inputs to AND,NAND logic Gates
    
    parent: parent object
    vectorInput: vector with booleans. Default [True,True]
                It's length is the number of inputs of the gate. 
                For each input (top to bottom) True: regular input  False: Negated input.
    position: position [x,y]
    label: label of the object (it can be repeated)
    """

    group = self.createGroup(parent,label)
        
    N_input=len(vectorInput)
    spaceBetweenInputs=20.0/(N_input-1)
    h_max=10 # maximum height of inputs
    
    for i in range(0, N_input):
      h=-(h_max-i*spaceBetweenInputs)
      self.createInput(vectorInput[i],group,[position[0], h+position[1]],0,'input' + str(i))
    
  #---------------------------------------------
  def createAND(self,parent,vectorInput=[True, True],output=True,position=[0, 0],label='BodyAND'):
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
    h=self.totalHeight/2.0 # half height
    R=h  # radius
    widthBase=self.totalWidth-2*self.lengthTerm-R # length of the straight part of AND body
    
    group = self.createGroup(parent,label)
    x_output = R # x coordinate of the output

    self.drawANDBody(group,position)
    self.drawInputAND(group,vectorInput,[-widthBase+position[0], position[1]])
    self.createOutput(output,group,[x_output+position[0], position[1]])
  #---------------------------------------------
  def createOR(self,parent,vectorInput=[True, True],output=True,position=[0, 0],label='ORGate'):
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
      
    group = self.createGroup(parent,label)
    x_output = self.totalHeight/2.0+5 # x coordinate of the output
    
    self.drawORBody(group,position)
    self.drawInputOR(group,vectorInput,[position[0]-15, position[1]])
    self.createOutput(output,group,[x_output+position[0], position[1]],-2.5) # 2.5 for reducing a little the lengh so that AND and

  #---------------------------------------------
  def createXOR(self,parent,vectorInput=[True, True],output=True,position=[0, 0],label='XORGate'):
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
      
    group = self.createGroup(parent,label)
    x_output = self.totalHeight/2.0+5 # x coordinate of the output
      
    self.drawXORBody(group,position)
    self.drawInputOR(group,vectorInput,[position[0]-15, position[1]])
    self.createOutput(output,group,[x_output+position[0], position[1]],-2.5) # 2.5 for reducing a little the lengh so that AND and
    
    #---------------------------------------------
  def createNOT(self,parent,position=[0, 0],label='NOTGate'):
    """ Creates NOT logic Gate
    
    parent: parent object
    vectorInput: vector with booleans. Default [True,True]
                It's length is the number of inputs of the gate. 
                For each input (top to bottom) True: regular input  False: Negated input.
    position: position [x,y]
    label: label of the object (it can be repeated)
    """
    
    triangleSide=20
    triangle_height=triangleSide*math.sqrt(3)/2
    
    group = self.createGroup(parent,label)  
    inkDraw.line.absCoords(group, [[0,triangleSide/2],[triangle_height,0],[0,-triangleSide/2],[0,triangleSide/2]], position,'not1',  self.lineStyleBody)
    
    self.createInput([True],group,position)
    self.createOutput(False,group,[triangle_height+0.5+position[0],0+position[1]],30-triangle_height-10-0.5)

    #---------------------------------------------
  def drawV(self,parent,position=[0, 0],label='GND',angleDeg=0,nodalVal='V_{cc}',drawLine=True):
    """ draws a Voltage node
    
    parent: parent object
    position: position [x,y]
    label: label of the object (it can be repeated)
    angleDeg: rotation angle in degrees counter-clockwise (default 0)
    nodalVal: name of the node (default: 'V_{cc}')
    drawLine: draws line for connection (default: True)
    """
    linestyleBlackFill=inkDraw.lineStyle.set(lineWidth=0.7,fillColor=inkDraw.color.defined('black'))
    group = self.createGroup(parent,label)
    elem = self.createGroup(group,label)
   
    inkDraw.circle.centerRadius(elem, position, 1.0, offset=[0,0],lineStyle=linestyleBlackFill)
    if drawLine: 
      inkDraw.line.relCoords(elem, [[0,10]],position)
      
    #text
    if abs(angleDeg)<=90:
      justif='bc'
      pos_text=[position[0],position[1]-self.textOffset]
    else:
      justif='tc'
      pos_text=[position[0],position[1]+self.textOffset]
    
    if not inkDraw.useLatex:
      value = nodalVal.replace('_','').replace('{','').replace('}','').replace(r'\volt','V')  # removes LaTeX stuff
    else:
      value = '$'+nodalVal+'$'
    temp=inkDraw.text.latex(self,group,value,pos_text,fontSize=self.fontSize,refPoint=justif,preambleFile=self.preambleFile)

    self.rotateElement(temp,position,-angleDeg)
    
    if angleDeg!=0:
      self.rotateElement(group,position,angleDeg)
      
    return group;
    
  #---------------------------------------------
  def drawGND(self,parent,position=[0, 0],label='GND',angleDeg=0):
    """ draws a GND
    
    parent: parent object
    position: position [x,y]
    label: label of the object (it can be repeated)
    angleDeg: rotation angle in degrees counter-clockwise (default 0)
    """

    group = self.createGroup(parent,label)
    elem = self.createGroup(group,label)
   
    inkDraw.line.relCoords(elem, [[0,10]],position)
    inkDraw.line.relCoords(elem, [[-14,0]],[position[0]+7,position[1]+10])
    inkDraw.line.relCoords(elem, [[-7,0]],[position[0]+3.5,position[1]+12])
    inkDraw.line.relCoords(elem, [[ -2,0]],[position[0]+1,position[1]+14])
           
    if angleDeg!=0:
      self.rotateElement(group,position,angleDeg)
      
    return group;
    
  #---------------------------------------------
  def drawCommon(self,parent,position=[0, 0],label='Common',angleDeg=0):
    """ draws a GND
    
    parent: parent object
    position: position [x,y]
    label: label of the object (it can be repeated)
    angleDeg: rotation angle in degrees counter-clockwise (default 0)
    """

    group = self.createGroup(parent,label)
    elem = self.createGroup(group,label)
   
    inkDraw.line.relCoords(elem, [[0,10]],position)
    inkDraw.line.relCoords(elem, [[-10,0],[5,5],[5,-5]],[position[0]+5,position[1]+10])
           
    if angleDeg!=0:
      self.rotateElement(group,position,angleDeg)
      
    return group;
  
  
  def createLatch(self,parent,position=[0, 0],label='Latch',type='SRnor',controlGate='none',controlGateLogic=True,asynPreset=0,asynClear=0):
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
    """
    group = self.createGroup(parent,label)
    
    if type=='SRnor' or type=='SRnand' or type=='JK':
      w=40
      h=50
      dist_signal=15
      y_controlGate=0
    
    if type=='D' or type=='T':
      w=40
      h=40
      dist_signal=10
      y_controlGate=10

    x_min=position[0]-w/2.0
    x_max=position[0]+w/2.0
    y_min=position[1]+h/2.0
    y_max=position[1]-h/2.0
    
    inkDraw.rectangle.widthHeightCenter(group, centerPoint=position, width=w, height=h,lineStyle=inkDraw.lineStyle.setSimpleBlack(1.5))
        
    self.createOutput(True,group,position=[x_max,position[1]-dist_signal],extraLength=0.0,label='Q',name='Q',fontSizeFactor=1.2)
    self.createOutput(True,group,position=[x_max,position[1]+dist_signal],extraLength=0.0,label='notQ',name='\NOT{Q}',fontSizeFactor=1.2)
    
    #Asyncronous Preset and Clear
    if asynPreset==1:
      self.createSignal(True,group,position=[position[0],y_max],direction='N',name='PRE',fontSizeFactor=0.8)
    elif asynPreset==-1:
      self.createSignal(False,group,position=[position[0],y_max],direction='N',name='PRE',fontSizeFactor=0.8)
      
    if asynClear==1:
      self.createSignal(True,group,position=[position[0],y_min],direction='S',name='CLR',fontSizeFactor=0.8)
    elif asynClear==-1:
      self.createSignal(False,group,position=[position[0],y_min],direction='S',name='CLR',fontSizeFactor=0.8)
    
    if controlGate=='level':
      self.createSignal(controlGateLogic,group,position=[x_min,position[1]+y_controlGate],direction='W',name='EN',isClock=False,fontSizeFactor=0.8)
    if controlGate=='edge':
      self.createSignal(controlGateLogic,group,position=[x_min,position[1]+y_controlGate],direction='W',name='CK',isClock=True,fontSizeFactor=0.8)
      
    if type=='SRnor' or type=='JK':
      self.createInput(True,group,position=[x_min,position[1]-dist_signal],extraLength=0.0,name=type[0],fontSizeFactor=1.2)
      self.createInput(True,group,position=[x_min,position[1]+dist_signal],extraLength=0.0,name=type[1],fontSizeFactor=1.2)
    elif type=='SRnand':
      input1=r'\NOT{%s}' % type[0]
      input2=r'\NOT{%s}' % type[1]
      self.createInput(True,group,position=[x_min,position[1]-dist_signal],extraLength=0.0,name=input1,fontSizeFactor=1.2)
      self.createInput(True,group,position=[x_min,position[1]+dist_signal],extraLength=0.0,name=input2,fontSizeFactor=1.2)
    elif type=='D' or type=='T':
      self.createInput(True,group,position=[x_min,position[1]-dist_signal],extraLength=0.0,name=type,fontSizeFactor=1.2)

if __name__ == '__main__':
  logic = LogicGates()
  logic.affect()
    