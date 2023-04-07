# Assume that 

# class FloatLiteral in AST is declared with field value in float type. 
# The visitor CodeGeneration has field emit keeping an object of Emitter 
# Object Frame is kept in field frame of the argument passed to parameter o of visitFloatLiteral
# The method visitFloatLiteral must return a pair of jasmin code of loading a float constant into operand stack and the type of the constant (one object of a subclass of class Type)
# Based on the above assumption, write method visitFloatLiteral(self,ctx,o) of visitor CodeGeneration? Your code is at line 160.
# Remind that class Type has subclasses: IntType, FloatType, VoidType, StringType.

def visitFloatLiteral(self, ctx, o):
        codegen = self.emit.emitPUSHFCONST(ctx.value, o.frame)
        return codegen, FloatType()