# Given the AST declarations as follows:

# class Program: #decl:List[VarDecl],exp:Exp

# class VarDecl: #name:str,typ:Type

# class Type(ABC): #abstract class

# class IntType(Type)

# class FloatType(Type)

# class BoolType(Type)

# class Exp(ABC): #abstract class

# class BinOp(Exp): #op:str,e1:Exp,e2:Exp #op is +,-,*,/,&&,||, >, <, ==, or  !=

# class UnOp(Exp): #op:str,e:Exp #op is -, !

# class IntLit(Exp): #val:int

# class FloatLit(Exp): #val:float

# class BoolLit(Exp): #val:bool

# class Id(Exp): #name:str

# and the Visitor class is declared as follows:

# class StaticCheck(Visitor):

#     def visitProgram(self,ctx:Program,o):pass

#     def visitVarDecl(self,ctx:VarDecl,o): pass

#     def visitIntType(self,ctx:IntType,o):pass

#     def visitFloatType(self,ctx:FloatType,o):pass

#     def visitBoolType(self,ctx:BoolType,o):pass

#     def visitBinOp(self,ctx:BinOp,o): pass

#     def visitUnOp(self,ctx:UnOp,o):pass

#     def visitIntLit(self,ctx:IntLit,o): pass 

#     def visitFloatLit(self,ctx,o): pass

#     def visitBoolLit(self,ctx,o): pass

#     def visitId(self,ctx,o): pass

# Rewrite the body of the methods in class StaticCheck to check the following type constraints:

# + , - and * accept their operands in int or float type and return float type if at least one of their operands is in float type, otherwise, return int type
# / accepts their operands in int or float type and returns float type
# !, && and || accept their operands in bool type and return bool type
# >, <, == and != accept their operands in any type but must in the same type and return bool type
# the type of an Id is from the declarations, if the Id is not in the declarations, exception UndeclaredIdentifier should be raised with the name of the Id. 

from abc import ABCMeta
class StaticCheck(Visitor):

    def visitProgram(self,ctx:Program,o):
        o = {}
        for x in ctx.decl: 
            o.update(self.visit(x,o))
        return self.visit(ctx.exp, o)

    def visitVarDecl(self,ctx:VarDecl,o):
        o[ctx.name] = ctx.typ
        return o

    def visitIntType(self,ctx:IntType,o):
        return IntType()

    def visitFloatType(self,ctx:FloatType,o):
        return FloatType()

    def visitBoolType(self,ctx:BoolType,o):
        return BoolType()

    def visitBinOp(self,ctx:BinOp,o):
        left_type = type(self.visit(ctx.e1,o))
        right_type = type(self.visit(ctx.e2,o))
        
        if ctx.op in ['+', '-', '*']:
            if BoolType in [left_type, right_type]:
                if left_type != right_type:
                    raise TypeMismatchInExpression(ctx)
                raise TypeMismatchInExpression(ctx)
            if FloatType in [left_type, right_type]:
                return FloatType()
            return IntType()
        elif ctx.op in ['/']:
            if BoolType in [left_type, right_type]:
                raise TypeMismatchInExpression(ctx)
            return FloatType()
        elif ctx.op in ['&&', '||']:
            if left_type == BoolType and right_type == BoolType:
                return BoolType()
            raise TypeMismatchInExpression(ctx)
        elif ctx.op in ['>', '<', '==', '!=']:
            if left_type != right_type:
                raise TypeMismatchInExpression(ctx)
            return BoolType()
            

    def visitUnOp(self,ctx:UnOp,o):
        param_type = self.visit(ctx.e, o)
        if ctx.op == '-':
            if type(param_type) == BoolType:
                raise TypeMismatchInExpression(ctx)
            return param_type
        elif ctx.op == '!':
            if type(param_type) != BoolType:
                raise TypeMismatchInExpression(ctx)
            return param_type

    def visitIntLit(self,ctx:IntLit,o):
        return IntType()

    def visitFloatLit(self,ctx,o):
        return FloatType()

    def visitBoolLit(self,ctx,o):
        return BoolType()

    def visitId(self,ctx,o):
        if ctx.name not in o:
            raise UndeclaredIdentifier(ctx.name)
        return o[ctx.name]
