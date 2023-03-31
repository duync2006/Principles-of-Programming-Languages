# Given the AST declarations as follows:

# class Exp(ABC): #abstract class

# class BinOp(Exp): #op:str,e1:Exp,e2:Exp #op is +,-,*,/,&&,||, >, <, ==, or  !=

# class UnOp(Exp): #op:str,e:Exp #op is -, !

# class IntLit(Exp): #val:int

# class FloatLit(Exp): #val:float

# class BoolLit(Exp): #val:bool

# and the Visitor class is declared as follows:

# class StaticCheck(Visitor):

#     def visitBinOp(self,ctx:BinOp,o): pass

#     def visitUnOp(self,ctx:UnOp,o):pass

#     def visitIntLit(self,ctx:IntLit,o): pass 

#     def visitFloatLit(self,ctx,o): pass

#     def visitBoolLit(self,ctx,o): pass

# Rewrite the body of the methods in class StaticCheck to check the following type constraints:

# + , - and * accept their operands in int or float type and return float type if at least one of their operands is in float type, otherwise, return int type
# / accepts their operands in int or float type and returns float type
# !, && and || accept their operands in bool type and return bool type
# >, <, == and != accept their operands in any type but must in the same type and return bool type 
# If the expression does not conform the type constraints, the StaticCheck will raise exception TypeMismatchInExpression with the innermost sub-expression that contains type mismatch.
class StaticCheck(Visitor):

    def visitBinOp(self,ctx:BinOp,o):
        left_type = (self.visit(ctx.e1,o))
        right_type = (self.visit(ctx.e2,o))
        
        if ctx.op in ['+', '-', '*']:
            if bool in [left_type, right_type]:
                raise TypeMismatchInExpression(ctx)
            if float in [left_type, right_type]:
                return type(float())
            return type(int())
        elif ctx.op in ['/']:
            if bool in [left_type, right_type]:
                raise TypeMismatchInExpression(ctx)
            return type(float())
        elif ctx.op in ['&&', '||']:
            if left_type == bool and right_type == bool:
                return type(bool())
            raise TypeMismatchInExpression(ctx)
        elif ctx.op in ['>', '<', '==', '!=']:
            if left_type != right_type:
                raise TypeMismatchInExpression(ctx)
            return type(bool())

    def visitUnOp(self,ctx:UnOp,o):
        param_type = self.visit(ctx.e, o)
        if ctx.op == '-':
            if param_type == bool:
                raise TypeMismatchInExpression(ctx)
            return param_type
        elif ctx.op == '!':
            if (param_type) != bool:
                raise TypeMismatchInExpression(ctx)
            return type(bool())

    def visitIntLit(self,ctx:IntLit,o):
        return type(ctx.val)

    def visitFloatLit(self,ctx,o):
        return type(ctx.val)

    def visitBoolLit(self,ctx,o):
        return type(ctx.val)  