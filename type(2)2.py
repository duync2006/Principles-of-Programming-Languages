# Given the AST declarations as follows:

# class Program: #decl:List[Decl],stmts:List[Stmt]

# class Decl(ABC): #abstract class

# class VarDecl(Decl): #name:str

# class FuncDecl(Decl): #name:str,param:List[VarDecl],local:List[Decl],stmts:List[Stmt]

# class Stmt(ABC): #abstract class

# class Assign(Stmt): #lhs:Id,rhs:Exp

# class CallStmt(Stmt): #name:str,args:List[Exp]

# class Exp(ABC): #abstract class

# class IntLit(Exp): #val:int

# class FloatLit(Exp): #val:float

# class BoolLit(Exp): #val:bool

# class Id(Exp): #name:str

# and the Visitor class is declared as follows:

# class StaticCheck(Visitor):

#     def visitProgram(self,ctx:Program,o):pass

#     def visitVarDecl(self,ctx:VarDecl,o): pass

#     def visitFuncDecl(self,ctx:FuncDecl,o): pass

#     def visitCallStmt(self,ctx:CallStmt,o):pass

#     def visitAssign(self,ctx:Assign,o): pass

#     def visitIntLit(self,ctx:IntLit,o): pass 

#     def visitFloatLit(self,ctx,o): pass

#     def visitBoolLit(self,ctx,o): pass

#     def visitId(self,ctx,o): pass

# Rewrite the body of the methods in class StaticCheck to infer the type of identifiers and check the following type constraints:

# In an Assign, the type of lhs must be the same as that of rhs, otherwise, the exception TypeMismatchInStatement should be raised together with the Assign
# the type of an Id is inferred from the above constraints in the first usage, 
# if the Id is not in the declarations, exception UndeclaredIdentifier should be raised together with the name of the Id, or
# If the Id cannot be inferred in the first usage, exception TypeCannotBeInferred should be raised together with the statement
# For static referencing environment, this language applies the scope rules of block-structured programming language where a function is a block. When there is a declaration duplication of a name in a scope, exception Redeclared should be raised together with the second declaration.
# In a call statement, the argument type must be the same as the parameter type. If there is no function declaration in the static referencing environment, exception UndeclaredIdentifier should be raised together with the function call name. If the numbers of parameters and arguments are not the same or at least one argument type is not the same as the type of the corresponding parameter, exception TypeMismatchInStatement should be raise with the call statement. If there is at least one parameter type cannot be resolved, exception TypeCannotBeInferred should be raised together with the call statement.

class IntType: pass
class FloatType: pass
class BoolType: pass

class StaticCheck(Visitor):
    # class Program: #decl:List[Decl],stmts:List[Stmt]
    def visitProgram(self,ctx:Program,o):
      o = []
      for x in ctx.decl:
         o.append(self.visit(x, o))
      for stmt in ctx.stmts: 
         self.visit(stmt, o)
    # class VarDecl(Decl): #name:str
    def visitVarDecl(self,ctx:VarDecl,o):
      if(self.lookup(ctx.name, o)): 
         raise Redeclared(ctx)
      return [ctx.name, None]

    # class FuncDecl(Decl): #name:str,param:List[VarDecl],local:List[Decl],stmts:List[Stmt]
    def visitFuncDecl(self,ctx:FuncDecl,o):
      if(self.lookup(ctx.name, o) != False): 
        raise Redeclared(ctx)
      param_decl = []
      local_decl = []
      for para in ctx.param:
         param_decl.append(self.visit(para, param_decl))
      for loc in ctx.local:
         local_decl.append(self.visit(loc, local_decl))
      for stmt in ctx.stmts:
         self.visit(stmt, param_decl + local_decl + o)
      return [ctx.name, param_decl]
      # [foo, [] ]
    # class CallStmt(Stmt): #name:str,args:List[Exp]
    def visitCallStmt(self,ctx:CallStmt,o):
      if(self.lookup(ctx.name,o) != False): 
        param_list = self.lookup(ctx.name,o)
        if type(param_list) is not list: 
           raise UndeclaredIdentifier(ctx.name)
        #  [[param_name1, type1], [param_name2, type2], ....]
        if len(ctx.args) != len(param_list):
          raise TypeMismatchInStatement(ctx)
        else: 
          for i in range(0, len(param_list)): 
            param_type = param_list[i][1]
            arg_type = self.visit(ctx.args[i],o)
            if param_type and arg_type: 
              if type(param_type) is not type(arg_type):
                raise TypeMismatchInStatement(ctx)
            elif not(param_type) and arg_type:
              #  update param_type
              param_list.append(arg_type)
              for name in param_list:
                 if name[0] == param_list[i][0]:
                    param_list[i][1] = param_list.pop()
                    break 
            elif not(arg_type) and param_type:
              # update arg_type 
              o.append(param_type)
              self.visit(ctx.args[i],o)
            else: 
                raise TypeCannotBeInferred(ctx)
      else: 
         raise UndeclaredIdentifier(ctx.name)

    # class Assign(Stmt): #lhs:Id,rhs:Exp
    def visitAssign(self,ctx:Assign,o):
        lhs_type = self.visit(ctx.lhs, o)
        rhs_type = self.visit(ctx.rhs, o)
        if lhs_type and rhs_type: 
          if type(lhs_type) is not type(rhs_type):
             raise TypeMismatchInStatement(ctx)
        elif lhs_type and not(rhs_type): 
          # update type for rhs
          o.append(lhs_type)
          self.visit(ctx.rhs, o)
        elif not(lhs_type) and rhs_type:
          # update type for lhs_type
          o.append(rhs_type)
          self.visit(ctx.lhs, o)
        else:
          raise TypeCannotBeInferred(ctx)

    def visitIntLit(self,ctx:IntLit,o):
      return IntType()

    def visitFloatLit(self,ctx,o):
      return FloatType()

    def visitBoolLit(self,ctx,o):
      return BoolType

    def visitId(self,ctx,o):
        for id in o:
            if id[0] == ctx.name:
                if type(o[-1]) in (IntType, FloatType, BoolType): 
                    id[1] = o.pop()
                    return None
                else:
                    return id[1]
        raise UndeclaredIdentifier(ctx.name)

    def lookup(self, name, o):
        for e in o:
            if name == e[0]: 
                return e[1]
        return False