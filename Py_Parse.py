
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
        return str(self.rule.orig) + " [ " + str(self.children) + " ] "
    def display(self, level = 0):
        """Used for printing out the tree"""
        print("|    " * level + str(self.rule.orig))
        for child in self.children:
            child.display(level+1)
    def bracket_repr(self): # http://ironcreek.net/phpsyntaxtree/?
        outstr = "[" + str(self.rule.orig) + " "
        outstr += ' '.join(child.bracket_repr() for child in self.children)
        outstr += "]"
        return outstr

class ParseException(Exception):
    """An exception raised if the parsing goes badly"""
    def __init__(self, stack):
        self.stack = stack
    def __str__(self):
        return "Error parsing input.\nEnd tree: " + str(self.stack)

def generate_tree(tokens, grammar ):
    """
        start_symbol,
        comment_start, comment_end,
        add_rule, neg_rule,
        mult_rule, pointer_rule,
        dec_sep_rule, dec_exp_symbol
    """
    """
        Generates a syntax tree out of a list of tokens.
        rules - A list of rules to apply. See rules.py.
        start_symbol - The start symbol in the list of rules.
        comment_start/end - The symbols that start/end a comment
        add_rule - The binary +/- rule
        neg_rule - The unary +/- rule
        mult_rule - The binary multiplication rule
        pointer_rule - The pointer rule
        dec_sep_rule - The base declaration separator rule
        dec_exp_symbol - The symbol for a declaration
    """
    """
        Create a parser.
    rules:
        A list of rules. Each rule is a `regex, type`
        pair, where `regex` is the regular expression used
        to recognize the token and `type` is the type
        of the token to return when it's recognized.
        skip_whitespace:
        If True, whitespace (\s+) will be skipped and not
        reported by the lexer. Otherwise, you have to
        specify your rules for whitespace, or it will be
        flagged as an error.
    """
    # All the regexes are concatenated into a single one
    # with named groups. Since the group names must be valid
    # Python identifiers, but the token types used by the
    # user are arbitrary strings, we auto-generate the group
    # names and map them to token types.
    #
    """
    idx = 1
    regex_parts = []
    self.group_type = {}
    
    for regex, type in grammar:
        groupname = 'GROUP%s' % idx
        regex_parts.append('(?P<%s>%s)' % (groupname, regex))
        self.group_type[groupname] = type
        idx += 1
    
    self.regex = re.compile('|'.join(regex_parts))
    self.skip_whitespace = skip_whitespace
    self.re_ws_skip = re.compile('\S')
    """

    # stores the stack of symbols for the bottom-up shift-reduce parser
    stack = ""
    # stores the tree itself in an analogous stack
    tree_stack = ""

    # We keep looping until none of the rules apply anymore and there are no
    # more tokens to inject into the stack.
    while True:
        print(stack) # great for debugging

        #skip_neg = False # don't apply the unary +/- rule if binary +/- skipped
        #skip_point = False # don't apply pointer rule if binary * skipped

        # Example of above:
        # If we have 3 + 4 * 5, we will skip applying add_rule to 3 + 4 because
        # * has higher priority. However, we then also need to skip applying the
        # unary + rule to the +4.
        for rule in grammar:
            # The rule can't possibly match if there are more symbols to match
            # than there are symbols in the stack
            gramm = re.compile(rule.value)
            if not gramm.search(stack): continue
            else:
                # check if the rule matches with the top of the stack
                m = gramm.search(stack)
                #print(m.group())
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
                        node = ParseNode(rule, tree_stack[m.start():])
                        print(node)
                        # simplify the tree stack
                        tree_stack = tree_stack[:m.start()] + str(node)
                        #ParseNode(rule,)
                        # simplify the stack
                        stack = stack[:m.start()] + rule.orig 
                        break # don't bother checking the rest of the rules
                        
        else: # none of the rules matched
            # if we're all out of tokens, we're done
            if not tokens: break
            else: # inject another token into the stack
                stack = stack+tokens[0].type
                tree_stack = tree_stack + tokens[0].type
                tokens = tokens[1:]
    
    # when we're done, we should have the start symbol left in the stack
    if stack == "FUNCT_DECLARE":
        return node.bracket_repr
        return 0
    else:
        raise ParseException(tree_stack)
