
"""
Parses the output of the lexer into a syntax tree. Currently uses a bottom-up
shift-reduce parsing algorithm. It's a touch ugly, but ShivC tries to avoid YACC
or the like.
"""

import re
class ParseNode:
    """A node in the parse tree. Each node represents the application of a
    particular grammar rule to a list of children nodes. Both are attributes."""
    def __init__(self, rule, children):
        self.rule = rule
        self.children = children
    def __repr__(self):
        s = ""
        for child in self.children:
            if(type(child) == ParseNode):
                s = s + str(child.rule.orig)
            else:
                s = s + child.val
            
        return str(self.rule.orig) + " [ " + s + " ] "
    def display(self, level = 0):
        """Used for printing out the tree"""
        print("|    " * level + str(self.rule.orig))
        for child in self.children:
            child.display(level+1)
    def bracket_repr(self): # http://ironcreek.net/phpsyntaxtree/?
        s = ""
        for child in self.children:
            if(type(child) == ParseNode):
                temp = child.bracket_repr()
                s = s + temp
            else:
                s = s + child.val
            
        outstr =  "<" + str(self.rule.orig) + ':' + str(self.rule.new) + ">" + " [ " + s + " ] "
        return outstr

class ParseException(Exception):
    """An exception raised if the parsing goes badly"""
    def __init__(self, stack):
        self.stack = stack
    def __str__(self):
        return "Error parsing input.\nEnd tree: " + str(self.stack)

def generate_tree(tokens, grammar, start_symbol ):
    """
        start_symbol,
        grammar,
        start_symbol
    """
    """
        Generates a syntax tree out of a list of tokens.
        rules - A list of rules to apply. See Py_Rules.py.
        start_symbol - The start symbol used as a placeholder for the stack.
    """
    """
        Create a parser.
    rules:
        A list of rules. See Py_Rules.py.Constructs parse tree using Rules 
        to shift-reduce parse the stack of tokens. The stack of tokens is 
        from the lexer. See Py_Lex.py.
    """
    
    # stores the stack of symbols for the bottom-up shift-reduce parser
    stack = ""
    # stores the tree itself in an analogous stack
    tree_stack = [start_symbol]
    """
        Loop through list of rules applying each to the current stack. If no
        rules match, shift on the next token to the stack.
    """
    while True:
        print(stack) # great for debugging
      
        for rule in grammar:
            # The rule can't possibly match if there are more symbols to match
            # than there are symbols in the stack
            gramm = re.compile(rule.value)
            # if rule is not present in stack, go to next rule
            if not gramm.search(stack): continue
            else:
                # check if the rule matches with the top of the stack
                m = gramm.search(stack)
                #print(m.group())
                
                # rule doesn't match 
                if not (m): break
                else:
                    # This rule matched!

                    # If the next token we'd inject has a higher priority than
                    # current rule, don't apply this rule

                    # Example: 3 + 4 * 5. When considering add_rule on 3 + 4, we
                    # should not apply this rule because we'll see tokens[0] is
                    # the asterisk, which has higher priority than the add rule.
                    if( rule.priority is not None
                        and len(tokens) > 0 and tokens[0].priority is not None
                        and tokens[0].priority < rule.priority ):
                            break
                    else:
                        
                        # we apply the rule!
                        temp = ""
                        
                        # Go back to check which token object is start of rule
                        for i, token in enumerate(tree_stack[::-1]):
                            # if the rule matches, this is the position for the stack
                            if(gramm.match(temp)):break
                            # special case if object is ParseNode    
                            if(type(token) != ParseNode ):
                                temp = token.type + temp
                            # case if object is Token
                            else:
                                temp = str(token.rule.orig) + temp
                            #print(temp)
                        print(i)
                        node = ParseNode(rule, tree_stack[-i:])
                        print(node)
                        # simplify the tree stack
                        tree_stack = tree_stack[:-i] + [node]
                        #ParseNode(rule,)
                        # simplify the stack
                        stack = stack[:m.start()] + rule.orig
                        break # don't bother checking the rest of the rules
                        
        else: # none of the rules matched
            # if we're all out of tokens, we're done
            if not tokens: break
            else: # push another token onto the stack
                stack = stack+tokens[0].type
                tree_stack.append(tokens[0])
                tokens = tokens[1:]
    
    # when we're done, we should have the start symbol (placeholder) left in the stack
    if tree_stack[0] == start_symbol:
        print(stack)
        return node
    else:
        raise ParseException(tree_stack)
