from immlib import *

class cc_hook(LogBpHook):
    
    def __init__(self):
        
        LogBpHook.__init__(self)
        self.imm = Debugger()
        
    def run(self,regs):

        self.imm.log(f"{regs['EIP']:08x}",regs['EIP'])
        self.imm.deleteBreakpoint(regs['EIP'])    
        
        return 
    
def main(args):
    
    imm = Debugger()

    calc = imm.getModule("calc.exe")
    imm.analyseCode(calc.getCodebase())

    functions = imm.getAllFunctions(calc.getCodebase())

    hooker = cc_hook()
    
    for function in functions:
        hooker.add(f"{function:08x}", function)
            
    return f"Tracking {len(functions)} functions."
