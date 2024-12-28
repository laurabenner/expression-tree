# Laura Benner
# Expression Tree Assignment
# December 6, 2024
# Enhancements made:
    # Allow free form use of spaces (including no spaces unless needed to separate two values)
    # Allow more than one input scheme auto-detecting the expression type (prefix, infix, and postfix input all supported)
    # Increase operator support (addition, multiplication, subtraction, division, modulus all supported)
    # Add narration routine using good English paragraph structure and ordinal words
    # Add an "evaluation order" counter (to the nodes) and show the order of operation execution
    # Some error handling and intelligent error messages


class ExprParser:
  def __init__(self, input):
    self.inputExpr = input.strip() # Remove leading and trailing whitespace from input

  # Returns single character values
  def getNext(self):
    self.inputExpr = self.inputExpr.strip() # Skip spaces
    if self.inputExpr:
      c = self.inputExpr[0]
      self.inputExpr = self.inputExpr[1:] # Remove c from inputExpr
      return c
    else:
      return None

class Node:
  def __init__(self, op, val=0, order=0): # Value and order default to zero
    self.op = op
    self.val = val
    self.order = order
    self.left = None
    self.right = None

  # Returns a prefix expression string
  def toPrefixString(self):
    if self.left and self.right: # If node has children, return operator followed by the output of recursive calls on the left and right child nodes
      s = self.op + " " + self.left.toPrefixString() + " " + self.right.toPrefixString()
      return s
    elif self.op == " ": # If node has no operator, return the value
      s = str(self.val)
      return s

  # Returns a postfix expression string
  def toPostfixString(self):
    if self.left and self.right: # If node has children, return the output of recursive calls on the left and right child nodes followed by the operator
      s = self.left.toPostfixString() + self.right.toPostfixString() + self.op + " "
      return s
    elif self.op == " ": # If node has no operator, return the value
      s = str(self.val) + " "
      return s

  # Returns an infix expression string
  def toInfixString(self):
    if self.left and self.right: # If node has children, return a parenthesized infix expression with the operator between the outputs of recursive calls on the left and right child nodes
      s = "(" + self.left.toInfixString() + " " + self.op + " " + self.right.toInfixString() + ")"
      return s
    elif self.op == " ": # If node has no operator, return the value
      s = str(self.val)
      return s

  # Returns a value and an order
  def evaluate(self, order=1):
    if order > 10:
      print("Error evaluating tree: too many operators")
      return None, 0
    if self.left and self.right: # If node has children:
      a, order = self.left.evaluate(order) # Set 'a' equal to the value of the left child node (determined by a recursive call)
      b, order = self.right.evaluate(order) # Set 'b' equal to the value of the right child node (determined by a recursive call)
      if a is None or b is None:
        return None, 0
      self.order = order # Set order of operation
      # Calculate and set the value of the operation
      if self.op == "+":
        self.val = a + b
      elif self.op == "*":
        self.val = a * b
      elif self.op == "-":
        self.val = a - b
      elif self.op == "/":
        if b == 0:
          print("Error evaluating tree: division by zero")
          return None, 0
        else:
          self.val = a / b
      elif self.op == "%":
        if b == 0:
          print("Error evaluating tree: modulo zero")
          return None, 0
        else:
          self.val = a % b
      return self.val, order+1 # Return value and incremented order
    elif self.op == " ": # If node has no operator, return the value and order
      return self.val, order

  # Delete tree
  def delete(self):
    if self.left and self.right:
      self.left.delete()
      self.right.delete()
      self.left = None
      self.right = None
    return

  # Returns a string with narration text
  def narrate(self, root, order=1):
    orderword = ["First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eigth", "Ninth", "Tenth"]
    descriptions = {
        " ": "the value ",
        "+": "the addition result of ",
        "*": "the multiplication result of ",
        "-": "the subtraction result of ",
        "/": "the division result of ",
        "%": "the modulus result of "
    }
    operations = {
          "+": " is added to ",
          "*": " is multiplied with ",
          "-": " is subtracted from ",
          "/": " is divided by ",
          "%": " is modulo "
    }
    s = "" # Initiate empty string
    if (self.order == order): # If order matches this node's order, narrate the operation
      s += "\n" + orderword[order - 1] + ", "
      s += descriptions.get(self.right.op, "") + str(round(self.right.val, 2))
      s += operations.get(self.op, "")
      s += descriptions.get(self.left.op, "") + str(round(self.left.val, 2))
      s += " to get " + str(round(self.val, 2)) + ". "
    elif (self.right and self.left): # Otherwise, perform recursive calls on the left and right children and add output narration to the string
      s += self.right.narrate(root, order) # Narrate right child
      if (s and self == root): # If any narration was produced from right child (correct order operation was found), and current node is the root: call narrate for the next operation in order
        s += self.narrate(root, order+1)
      else: # Otherwise, narrate left child
        s += self.left.narrate(root, order)
        if (s and self == root): # If any narration was produced from left child (currect order operation was found), and current node is the root: call narrate for the next operation in order
          s += self.narrate(root, order+1)
    return s # Return the string; if there are no children the string will be empty

  # Prints the tree
  def printTree(self, level):
    suffixes = ["st", "nd", "rd", "th", "th", "th", "th", "th", "th", "th"] # List with ordinal suffixes
    if self.right and self.left: # If current node has children, print the next level of the tree with increased indentation
      self.right.printTree(level+10)
      print(str(self.order) + suffixes[self.order-1] + " " + " " * level + self.op + "(" + str(round(self.val, 2)) + ")") # Print order, operation, and value
      self.left.printTree(level+10)
    elif self.op == " ": # If current node has no operator, print the value, rounded to two decimal places and indented from the left
      print("    " + " " * level + str(round(self.val, 2)))


class ExprTree:
  def __init__(self):
    self.root = None

  # Builds tree from a prefix expression
  def buildFromPrefixExpression(self, expr):
    c = expr.getNext() # Retrieve next character and remove it from expr
    if (c == "+" or c=="*" or c=="-" or c=="/" or c=="%"): # If c is a supported operation, create a new node and assign it left and right child nodes with recursive calls on expr; return the node
      root = Node(c)
      root.left = self.buildFromPrefixExpression(expr)
      root.right = self.buildFromPrefixExpression(expr)
      if root.left and root.right:
        return root
      else: # If an unexpected character was found, return None
        return None
    elif c.isdigit(): # If c is a digit, create a new node with no operator and c as its value
      return Node(' ', int(c))
    else: # If c is neither a supported operator or a digit, return none
      print(f"Unexpected character: {c}")
      return None

  # Builds tree from a postfix expression
  def buildFromPostfixExpression(self, expr):
    stack = [] # Initialize empty stack
    c = expr.getNext() # Retrieve next character and remove it from expr
    while c: # While there are still characters in the expression:
      if c.isdigit(): # If c is a digit, create a new node with no operator and c as its value; push it onto the stack
        stack.append(Node(' ', int(c)))
      elif (c == "+" or c=="*" or c=="-" or c=="/" or c=="%"): # If c is a supported operation, create a new node and assign it left and right child nodes by popping nodes off the stack; push this node onto the stack
        root = Node(c)
        root.right = stack.pop()
        root.left = stack.pop()
        stack.append(root)
      else: # If c is neither a supported operator or a digit, return none
        print(f"Unexpected character: {c}")
        return None
      c = expr.getNext() # Retrieve next character and remove it from expr
    return stack.pop() # At end of expr, return root node

  # Builds tree from an infix expression
  def buildFromInfixExpression(self, expr):
    stack = [] # Initialize empty stack
    c = expr.getNext() # Retrieve next character and remove it from expr
    while c: # While there are still characters in the expression
      if (c == "("): # If c is a left parenthesis, make a recursive call on expr and push the node it returns onto the stack
        root = self.buildFromInfixExpression(expr)
        if root:
          stack.append(root)
        else:
          return None
      elif c.isdigit(): # If c is a digit, create a new node with no operator and c as its value; push it onto the stack
        stack.append(Node(' ', int(c)))
      elif (c == "+" or c=="*" or c=="-" or c=="/" or c=="%"): # If c is a supported operation, create a new node
        root = Node(c)
        root.left = stack.pop() # Assign a left child by popping a node off the stack
        root.right = self.buildFromInfixExpression(expr) # Assign a right child by making a recursive call on expr
        if root.left and root.right:
          return root
        else: # If an unexpected character was found, return none
          return None
      elif (c == ")"): # If c is a right parenthesis, return the node at the top of the stack
        return stack.pop()
      else: # If c is not a parenthesis, supported operator, or digit, return none
        print(f"Unexpected character: {c}")
        return None
      c = expr.getNext() # Retrieve next character and remove it from expr
    return stack.pop() # At the end of expr, return the last node on the stack

  # Autodetect expression type and fill tree
  def fillFromExpression(self, expr):
    if (len(expr.inputExpr) == 0):
      print("Empty input")
    else:
      c = expr.inputExpr[0] # Get first character of expression; use to call appropriate function
      if (c == "+" or c=="*" or c=="-" or c=="/" or c=="%"):
        try:
          self.root = self.buildFromPrefixExpression(expr)
        except:
          print("Unexpected input")
      elif (c.isdigit()):
        try:
          self.root = self.buildFromPostfixExpression(expr)
        except:
          print("Unexpected input")
      elif (c == "("):
        try:
          self.root = self.buildFromInfixExpression(expr)
        except:
          print("Unexpected input")
      else:
        print(f"Unexpected character: {c}")

  # Return tree as prefix string
  def toPrefixString(self):
    if self.root:
      return self.root.toPrefixString() + "\n"
    return "\n"

  # Return tree as postfix string
  def toPostfixString(self):
    if self.root:
      return self.root.toPostfixString() + "\n"
    return "\n"

  # Return tree as infix string
  def toInfixString(self):
    if self.root:
      return self.root.toInfixString() + "\n"
    return "\n"

  # Evaluate tree and return final value rounded to 2 decimal places
  def evaluate(self):
    if self.root:
      value = self.root.evaluate()[0]
      if value:
        return str(round(value, 2)) + "\n"
      else:
        self.delete()
        return "\n"
    return "\n"

  # Delete tree
  def delete(self):
    if self.root:
        self.root.delete()
        self.root = None

  # Return narration text for tree's evaluation process
  def narrate(self):
    if self.root:
      self.evaluate()
      return self.root.narrate(self.root) + "\n" + "The value of the entire expression is " + str(self.root.val) + "."
    return "\n"

  # Print tree
  def printTree(self):
    if self.root:
      self.evaluate()
      print("Order")
      self.root.printTree(0)
    print("\n")


inputExpr = ExprParser(input("Enter an expression (limit to 10 operators): "))
myTree = ExprTree()
myTree.fillFromExpression(inputExpr)

print()
print("Prefix string: " + myTree.toPrefixString())
print("Postfix string: " + myTree.toPostfixString())
print("Infix string: " + myTree.toInfixString())
print("Expression value: " + myTree.evaluate())
myTree.printTree()
print("Full English narration: " + myTree.narrate())