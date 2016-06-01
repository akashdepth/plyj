# Base node
class SourceElement(object):
    '''
    A SourceElement is the base class for all elements that occur in a Java
    file parsed by plyj.
    '''
    
    def __init__(self):
        super(SourceElement, self).__init__()
        self._fields = []
        

    def __repr__(self):
        equals = ("{0}={1!r}".format(k, getattr(self, k))
                  for k in self._fields)
        args = ", ".join(equals)
        return "{0}({1})".format(self.__class__.__name__, args)

    def __eq__(self, other):
        try:
            return self.__dict__ == other.__dict__
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self == other

    def accept(self, visitor):
        """
        default implementation that visit the subnodes in the order
        they are stored in self_field
        """
        class_name = self.__class__.__name__
        visit = getattr(visitor, 'visit_' + class_name)
        if visit(self):
            for f in self._fields:
                field = getattr(self, f)
                if field:
                    if isinstance(field, list):
                        for elem in field:
                            if isinstance(elem, SourceElement):
                                elem.accept(visitor)
                    elif isinstance(field, SourceElement):
                        field.accept(visitor)
        getattr(visitor, 'leave_' + class_name)(self)


class CompilationUnit(SourceElement):

    def __init__(self, package_declaration=None, import_declarations=None,
                 type_declarations=None,lineno=1):
        super(CompilationUnit, self).__init__()
        self._fields = [
            'package_declaration', 'import_declarations', 'type_declarations']
        if import_declarations is None:
            import_declarations = []
        if type_declarations is None:
            type_declarations = []
        self.package_declaration = package_declaration
        self.import_declarations = import_declarations
        self.type_declarations = type_declarations
        self.lineno = lineno
class PackageDeclaration(SourceElement):

    def __init__(self, name, modifiers=None,lineno=1):
        super(PackageDeclaration, self).__init__()
        self._fields = ['name', 'modifiers']
        if modifiers is None:
            modifiers = []
        self.name = name
        self.modifiers = modifiers
        self.lineno = lineno

class ImportDeclaration(SourceElement):

    def __init__(self, name, static=False, on_demand=False):
        super(ImportDeclaration, self,lineno=1).__init__()
        self._fields = ['name', 'static', 'on_demand']
        self.name = name
        self.static = static
        self.on_demand = on_demand
        self.lineno = lineno

class ClassDeclaration(SourceElement):

    def __init__(self, name, body, modifiers=None, type_parameters=None,
                 extends=None, implements=None,lineno=1):
        super(ClassDeclaration, self).__init__()
        self._fields = ['name', 'body', 'modifiers',
                        'type_parameters', 'extends', 'implements']
        if modifiers is None:
            modifiers = []
        if type_parameters is None:
            type_parameters = []
        if implements is None:
            implements = []
        self.name = name
        self.body = body
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.extends = extends
        self.implements = implements
        self.lineno = lineno
class ClassInitializer(SourceElement):

    def __init__(self, block, static=False,lineno=1):
        super(ClassInitializer, self).__init__()
        self._fields = ['block', 'static']
        self.block = block
        self.static = static
        self.lineno = lineno

class ConstructorDeclaration(SourceElement):

    def __init__(self, name, block, modifiers=None, type_parameters=None,
                 parameters=None, throws=None,lineno=1):
        super(ConstructorDeclaration, self).__init__()
        self._fields = ['name', 'block', 'modifiers',
                        'type_parameters', 'parameters', 'throws']
        if modifiers is None:
            modifiers = []
        if type_parameters is None:
            type_parameters = []
        if parameters is None:
            parameters = []
        self.name = name
        self.block = block
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.parameters = parameters
        self.throws = throws
        self.lineno = lineno

class EmptyDeclaration(SourceElement):
    pass

class FieldDeclaration(SourceElement):

    def __init__(self, type, variable_declarators, modifiers=None,lineno=1):
        super(FieldDeclaration, self).__init__()
        self._fields = ['type', 'variable_declarators', 'modifiers']
        if modifiers is None:
            modifiers = []
        self.type = type
        self.variable_declarators = variable_declarators
        self.modifiers = modifiers
        self.lineno = lineno

class MethodDeclaration(SourceElement):

    def __init__(self, name, modifiers=None, type_parameters=None,
                 parameters=None, return_type='void', body=None, abstract=False,
                 extended_dims=0, throws=None,lineno =1):
        super(MethodDeclaration, self).__init__()
        self._fields = ['name', 'modifiers', 'type_parameters', 'parameters',
                        'return_type', 'body', 'abstract', 'extended_dims',
                        'throws']
        if modifiers is None:
            modifiers = []
        if type_parameters is None:
            type_parameters = []
        if parameters is None:
            parameters = []
        self.name = name
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.parameters = parameters
        self.return_type = return_type
        self.body = body
        self.abstract = abstract
        self.extended_dims = extended_dims
        self.throws = throws
        self.lineno = lineno

class FormalParameter(SourceElement):

    def __init__(self, variable, type, modifiers=None, vararg=False,lineno=1):
        super(FormalParameter, self).__init__()
        self._fields = ['variable', 'type', 'modifiers', 'vararg']
        if modifiers is None:
            modifiers = []
        self.variable = variable
        self.type = type
        self.modifiers = modifiers
        self.vararg = vararg
        self.lineno = lineno


class Variable(SourceElement):
    # I would like to remove this class. In theory, the dimension could be added
    # to the type but this means variable declarations have to be changed
    # somehow. Consider 'int i, j[];'. In this case there currently is only one
    # type with two variable declarators;This closely resembles the source code.
    # If the variable is to go away, the type has to be duplicated for every
    # variable...

    def __init__(self, name, dimensions=0,lineno=1):
        super(Variable, self).__init__()
        self._fields = ['name', 'dimensions']
        self.name = name
        self.dimensions = dimensions
        self.lineno = lineno


class VariableDeclarator(SourceElement):

    def __init__(self, variable, initializer=None,lineno=1):
        super(VariableDeclarator, self).__init__()
        self._fields = ['variable', 'initializer']
        self.variable = variable
        self.initializer = initializer
        self.lineno = lineno

class Throws(SourceElement):

    def __init__(self, types,lineno=1):
        super(Throws, self).__init__()
        self._fields = ['types']
        self.types = types
        self.lineno = lineno

class InterfaceDeclaration(SourceElement):

    def __init__(self, name, modifiers=None, extends=None, type_parameters=None,
                 body=None,lineno=1):
        super(InterfaceDeclaration, self).__init__()
        self._fields = [
            'name', 'modifiers', 'extends', 'type_parameters', 'body']
        if modifiers is None:
            modifiers = []
        if extends is None:
            extends = []
        if type_parameters is None:
            type_parameters = []
        if body is None:
            body = []
        self.name = name
        self.modifiers = modifiers
        self.extends = extends
        self.type_parameters = type_parameters
        self.body = body
        self.lineno = lineno

class EnumDeclaration(SourceElement):

    def __init__(self, name, implements=None, modifiers=None,
                 type_parameters=None, body=None,lineno=1):
        super(EnumDeclaration, self).__init__()
        self._fields = [
            'name', 'implements', 'modifiers', 'type_parameters', 'body']
        if implements is None:
            implements = []
        if modifiers is None:
            modifiers = []
        if type_parameters is None:
            type_parameters = []
        if body is None:
            body = []
        self.name = name
        self.implements = implements
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.body = body
        self.lineno = lineno

class EnumConstant(SourceElement):

    def __init__(self, name, arguments=None, modifiers=None, body=None,lineno=1):
        super(EnumConstant, self).__init__()
        self._fields = ['name', 'arguments', 'modifiers', 'body','lineno']
        if arguments is None:
            arguments = []
        if modifiers is None:
            modifiers = []
        if body is None:
            body = []
        self.name = name
        self.arguments = arguments
        self.modifiers = modifiers
        self.body = body
        self.lineno = lineno

class AnnotationDeclaration(SourceElement):

    def __init__(self, name, modifiers=None, type_parameters=None, extends=None,
                 implements=None, body=None,lineno=1):
        super(AnnotationDeclaration, self).__init__()
        self._fields = [
            'name', 'modifiers', 'type_parameters', 'extends', 'implements',
            'body','lineno']
        if modifiers is None:
            modifiers = []
        if type_parameters is None:
            type_parameters = []
        if implements is None:
            implements = []
        if body is None:
            body = []
        self.name = name
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.extends = extends
        self.implements = implements
        self.body = body
        self.lineno = lineno

class AnnotationMethodDeclaration(SourceElement):

    def __init__(self, name, type, parameters=None, default=None,
                 modifiers=None, type_parameters=None, extended_dims=0,lineno=1):
        super(AnnotationMethodDeclaration, self).__init__()
        self._fields = ['name', 'type', 'parameters', 'default',
                        'modifiers', 'type_parameters', 'extended_dims','lineno']
        if parameters is None:
            parameters = []
        if modifiers is None:
            modifiers = []
        if type_parameters is None:
            type_parameters = []
        self.name = name
        self.type = type
        self.parameters = parameters
        self.default = default
        self.modifiers = modifiers
        self.type_parameters = type_parameters
        self.extended_dims = extended_dims
        self.lineno = lineno

class Annotation(SourceElement):

    def __init__(self, name, members=None, single_member=None,lineno=1):
        super(Annotation, self).__init__()
        self._fields = ['name', 'members', 'single_member','lineno']
        if members is None:
            members = []
        self.name = name
        self.members = members
        self.single_member = single_member
        self.lineno = lineno


class AnnotationMember(SourceElement):

    def __init__(self, name, value,lineno=1):
        super(SourceElement, self).__init__()
        self._fields = ['name', 'value','lineno']
        self.name = name
        self.value = value
        self.lineno = lineno


class Type(SourceElement):

    def __init__(self, name, type_arguments=None, enclosed_in=None,
                 dimensions=0,lineno=1):
        super(Type, self).__init__()
        self._fields = ['name', 'type_arguments', 'enclosed_in', 'dimensions','lineno']
        if type_arguments is None:
            type_arguments = []
        self.name = name
        self.type_arguments = type_arguments
        self.enclosed_in = enclosed_in
        self.dimensions = dimensions
        self.lineno = lineno


class Wildcard(SourceElement):

    def __init__(self, bounds=None,lineno=1):
        super(Wildcard, self).__init__()
        self._fields = ['bounds','lineno']
        if bounds is None:
            bounds = []
        self.bounds = bounds
        self.lineno = lineno


class WildcardBound(SourceElement):

    def __init__(self, type, extends=False, _super=False,lineno=1):
        super(WildcardBound, self).__init__()
        self._fields = ['type', 'extends', '_super','lineno']
        self.type = type
        self.extends = extends
        self._super = _super


class TypeParameter(SourceElement):

    def __init__(self, name, extends=None,lineno=1):
        super(TypeParameter, self).__init__()
        self._fields = ['name', 'extends','lineno']
        if extends is None:
            extends = []
        self.name = name
        self.extends = extends
        self.lineno = lineno


class Expression(SourceElement):

    def __init__(self,lineno=1):
        super(Expression, self).__init__()
        self._fields = ['lineno']
        self.lineno = lineno

class BinaryExpression(Expression):

    def __init__(self, operator, lhs, rhs,lineno=1):
        super(BinaryExpression, self).__init__()
        self._fields = ['operator', 'lhs', 'rhs','lineno']
        self.operator = operator
        self.lhs = lhs
        self.rhs = rhs
        self.lineno = lineno

class Assignment(BinaryExpression):
    pass


class Conditional(Expression):

    def __init__(self, predicate, if_true, if_false,lineno=1):
        super(self.__class__, self).__init__()
        self._fields = ['predicate', 'if_true', 'if_false','lineno']
        self.predicate = predicate
        self.if_true = if_true
        self.if_false = if_false
        self.lineno = lineno

class ConditionalOr(BinaryExpression):
    pass

class ConditionalAnd(BinaryExpression):
    pass

class Or(BinaryExpression):
    pass


class Xor(BinaryExpression):
    pass


class And(BinaryExpression):
    pass


class Equality(BinaryExpression):
    pass


class InstanceOf(BinaryExpression):
    pass


class Relational(BinaryExpression):
    pass


class Shift(BinaryExpression):
    pass


class Additive(BinaryExpression):
    pass


class Multiplicative(BinaryExpression):
    pass


class Unary(Expression):

    def __init__(self, sign, expression,lineno=1,lineno=1):
        super(Unary, self).__init__()
        self._fields = ['sign', 'expression','lineno']
        self.sign = sign
        self.expression = expression
        self.lineno = lineno


class Cast(Expression):

    def __init__(self, target, expression,lineno=1):
        super(Cast, self).__init__()
        self._fields = ['target', 'expression','lineno']
        self.target = target
        self.expression = expression
        self.lineno = lineno


class Statement(SourceElement):
    pass

class Empty(Statement):
    pass


class Block(Statement):

    def __init__(self, statements=None,lineno=1):
        super(Statement, self).__init__()
        self._fields = ['statements','lineno','lineno']
        if statements is None:
            statements = []
        self.statements = statements
        self.lineno = lineno

    def __iter__(self):
        for s in self.statements:
            yield s

class VariableDeclaration(Statement, FieldDeclaration):
    pass

class ArrayInitializer(SourceElement):
    def __init__(self, elements=None,lineno=1):
        super(ArrayInitializer, self).__init__()
        self._fields = ['elements','lineno']
        if elements is None:
            elements = []
        self.elements = elements
        self.lineno = lineno


class MethodInvocation(Expression):
    def __init__(self, name, arguments=None, type_arguments=None, target=None,lineno=1):
        super(MethodInvocation, self).__init__()
        self._fields = ['name', 'arguments', 'type_arguments', 'target','lineno']
        if arguments is None:
            arguments = []
        if type_arguments is None:
            type_arguments = []
        self.name = name
        self.arguments = arguments
        self.type_arguments = type_arguments
        self.target = target
        self.lineno = lineno

class IfThenElse(Statement):

    def __init__(self, predicate, if_true=None, if_false=None,lineno=1):
        super(IfThenElse, self).__init__()
        self._fields = ['predicate', 'if_true', 'if_false','lineno']
        self.predicate = predicate
        self.if_true = if_true
        self.if_false = if_false
        self.lineno = lineno

class While(Statement):

    def __init__(self, predicate, body=None,lineno=1):
        super(While, self).__init__()
        self._fields = ['predicate', 'body','lineno']
        self.predicate = predicate
        self.body = body
        self.lineno = lineno

class For(Statement):

    def __init__(self, init, predicate, update, body,lineno=1):
        super(For, self).__init__()
        self._fields = ['init', 'predicate', 'update', 'body','lineno','lineno']
        self.init = init
        self.predicate = predicate
        self.update = update
        self.body = body
        self.lineno = lineno

class ForEach(Statement):

    def __init__(self, type, variable, iterable, body, modifiers=None,lineno=1):
        super(ForEach, self).__init__()
        self._fields = ['type', 'variable', 'iterable', 'body', 'modifiers','lineno']
        if modifiers is None:
            modifiers = []
        self.type = type
        self.variable = variable
        self.iterable = iterable
        self.body = body
        self.modifiers = modifiers
        self.lineno = lineno


class Assert(Statement):

    def __init__(self, predicate, message=None,lineno=1):
        super(Assert, self).__init__()
        self._fields = ['predicate', 'message','lineno']
        self.predicate = predicate
        self.message = message
        self.lineno = lineno


class Switch(Statement):

    def __init__(self, expression, switch_cases,lineno=1):
        super(Switch, self).__init__()
        self._fields = ['expression', 'switch_cases','lineno']
        self.expression = expression
        self.switch_cases = switch_cases
        self.lineno = lineno

class SwitchCase(SourceElement):

    def __init__(self, cases, body=None,lineno=1):
        super(SwitchCase, self).__init__()
        self._fields = ['cases', 'body','lineno']
        if body is None:
            body = []
        self.cases = cases
        self.body = body
        self.lineno = lineno

class DoWhile(Statement):

    def __init__(self, predicate, body=None,lineno=1,lineno=1):
        super(DoWhile, self).__init__()
        self._fields = ['predicate', 'body','lineno']
        self.predicate = predicate
        self.body = body
        self.lineno = lineno


class Continue(Statement):

    def __init__(self, label=None,lineno=1):
        super(Continue, self).__init__()
        self._fields = ['label','lineno','lineno']
        self.label = label
        self.lineno = lineno


class Break(Statement):

    def __init__(self, label=None,lineno=1):
        super(Break, self).__init__()
        self._fields = ['label','lineno']
        self.label = label
        self.lineno = lineno


class Return(Statement):

    def __init__(self, result=None,lineno=1):
        super(Return, self).__init__()
        self._fields = ['result','lineno','lineno']
        self.result = result
        self.lineno = lineno


class Synchronized(Statement):

    def __init__(self, monitor, body,lineno=1):
        super(Synchronized, self).__init__()
        self._fields = ['monitor', 'body','lineno']
        self.monitor = monitor
        self.body = body
        self.lineno = lineno


class Throw(Statement):

    def __init__(self, exception,lineno=1):
        super(Throw, self).__init__()
        self._fields = ['exception','lineno']
        self.exception = exception
        self.lineno = lineno


class Try(Statement):

    def __init__(self, block, catches=None, _finally=None, resources=None,lineno=1):
        super(Try, self).__init__()
        self._fields = ['block', 'catches', '_finally', 'resources','lineno']
        if catches is None:
            catches = []
        if resources is None:
            resources = []
        self.block = block
        self.catches = catches
        self._finally = _finally
        self.resources = resources
        self.lineno = lineno

    def accept(self, visitor):
        if visitor.visit_Try(self):
            for s in self.block:
                s.accept(visitor)
        for c in self.catches:
            visitor.visit_Catch(c)
        if self._finally:
            self._finally.accept(visitor)


class Catch(SourceElement):

    def __init__(self, variable, modifiers=None, types=None, block=None,lineno=1):
        super(Catch, self).__init__()
        self._fields = ['variable', 'modifiers', 'types', 'block','lineno']
        if modifiers is None:
            modifiers = []
        if types is None:
            types = []
        self.variable = variable
        self.modifiers = modifiers
        self.types = types
        self.block = block
        self.lineno = lineno


class Resource(SourceElement):

    def __init__(self, variable, type=None, modifiers=None, initializer=None,lineno=1):
        super(Resource, self).__init__()
        self._fields = ['variable', 'type', 'modifiers', 'initializer','lineno']
        if modifiers is None:
            modifiers = []
        self.variable = variable
        self.type = type
        self.modifiers = modifiers
        self.initializer = initializer
        self.lineno = lineno


class ConstructorInvocation(Statement):
    """An explicit invocations of a class's constructor.

    This is a variant of either this() or super(), NOT a "new" expression.
    """

    def __init__(self, name, target=None, type_arguments=None, arguments=None,lineno=1):
        super(ConstructorInvocation, self).__init__()
        self._fields = ['name', 'target', 'type_arguments', 'arguments','lineno','lineno']
        if type_arguments is None:
            type_arguments = []
        if arguments is None:
            arguments = []
        self.name = name
        self.target = target
        self.type_arguments = type_arguments
        self.arguments = arguments
        self.lineno = lineno


class InstanceCreation(Expression):

    def __init__(self, type, type_arguments=None, arguments=None, body=None,
                 enclosed_in=None,lineno=1):
        super(InstanceCreation, self).__init__()
        self._fields = [
            'type', 'type_arguments', 'arguments', 'body', 'enclosed_in','lineno']
        if type_arguments is None:
            type_arguments = []
        if arguments is None:
            arguments = []
        if body is None:
            body = []
        self.type = type
        self.type_arguments = type_arguments
        self.arguments = arguments
        self.body = body
        self.enclosed_in = enclosed_in
        self.lineno = lineno


class FieldAccess(Expression):

    def __init__(self, name, target,lineno=1):
        super(FieldAccess, self).__init__()
        self._fields = ['name', 'target','lineno']
        self.name = name
        self.target = target
        self.lineno = lineno


class ArrayAccess(Expression):

    def __init__(self, index, target,lineno=1):
        super(ArrayAccess, self).__init__()
        self._fields = ['index', 'target','lineno']
        self.index = index
        self.target = target
        self.lineno = lineno


class ArrayCreation(Expression):

    def __init__(self, type, dimensions=None, initializer=None,lineno=1):
        super(ArrayCreation, self).__init__()
        self._fields = ['type', 'dimensions', 'initializer','lineno']
        if dimensions is None:
            dimensions = []
        self.type = type
        self.dimensions = dimensions
        self.initializer = initializer
        self.lineno = lineno


class Literal(SourceElement):

    def __init__(self, value,lineno=1):
        super(Literal, self).__init__()
        self._fields = ['value','lineno']
        self.value = value
        self.lineno = lineno


class ClassLiteral(SourceElement):

    def __init__(self, type,lineno=1,lineno=1:
        super(ClassLiteral, self).__init__()
        self._fields = ['type','lineno']
        self.type = type
        self.lineno = lineno


class Name(SourceElement):

    def __init__(self, value,lineno=1):
        super(Name, self).__init__()
        self._fields = ['value','lineno']
        self.value = value
        self.lineno = lineno

    def append_name(self, name):
        try:
            self.value = self.value + '.' + name.value
        except:
            self.value = self.value + '.' + name


class ExpressionStatement(Statement):
    def __init__(self, expression,lineno=1):
        super(ExpressionStatement, self).__init__()
        self._fields = ['expression','lineno']
        self.expression = expression
        self.lineno = lineno


class Visitor(object):

    def __init__(self, verbose=False):
        self.verbose = verbose

    def __getattr__(self, name):
        if not (name.startswith('visit_') or name.startswith('leave_')):
            raise AttributeError('name must start with visit_ or leave_ but was {}'
                                 .format(name))

        def f(element):
            if self.verbose:
                msg = 'unimplemented call to {}; ignoring ({})'
                print(msg.format(name, element))
            return True
        return f

