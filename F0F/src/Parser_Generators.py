from F0FGrammar import Terminal, NonTerminal, Production, Sentential_Form, Symbol, EOF, Epsilon, Grammar, F0F_LL_1
from F0FTokens import Token, TokenType, NonTerminalsTokens

class ContainerSet:
    def __init__(self, *values, contains_epsilon=False):
        self.set = set(values)
        self.contains_epsilon = contains_epsilon

    def add(self, value):
        n = len(self.set)
        self.set.add(value)
        return n != len(self.set)

    def extend(self, values):
        change = False
        for value in values:
            change |= self.add(value)
        return change

    def set_epsilon(self, value=True):
        last = self.contains_epsilon
        self.contains_epsilon = value
        return last != self.contains_epsilon

    def update(self, other):
        n = len(self.set)
        self.set.update(other.set)
        return n != len(self.set)

    def epsilon_update(self, other):
        return self.set_epsilon(self.contains_epsilon | other.contains_epsilon)

    def hard_update(self, other):
        return self.update(other) | self.epsilon_update(other)

    def find_match(self, match):
        for item in self.set:
            if item == match:
                return item
        return None

    def __len__(self):
        return len(self.set) + int(self.contains_epsilon)

    def __str__(self):
        return '%s-%s' % (str(self.set), self.contains_epsilon)

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return iter(self.set)

    def __nonzero__(self):
        return len(self) > 0

    def __eq__(self, other):
        if isinstance(other, set):
            return self.set == other
        return isinstance(other, ContainerSet) and self.set == other.set and self.contains_epsilon == other.contains_epsilon

def First(grammar:Grammar):
    firsts = {}
    
    for t in grammar.terminals:         # First(Vt)
        firsts[t] = ContainerSet(t)
    for nt in grammar.nonTerminals:     # init First(Vn)
        firsts[nt] = ContainerSet()
    change = True
    while change:
        change = False
        for pr in grammar.Productions:
            # X -> alpha
            pr:Production
            X = pr.Head
            alpha = pr.Body
            """ The set First for an sentential form is:
                First(SF) = { x in Vt | SF ->* xa, a in (Vt or Vn)*} 
                including epsilon if SF ->* epsilon
            """
            if alpha.IsEpsilon:
                firsts[alpha] = ContainerSet(contains_epsilon= True)
                change  = change or firsts[X].set_epsilon()
            else:
                # its a sentential form
                # if len(alpha) <= 1:
                #     # only one non-terminal
                #     alpha = alpha[0]
                try:
                    f_alpha = firsts[alpha]                    
                except KeyError:
                    firsts[alpha] = ContainerSet()
                
                local_first = sentential_first(firsts, alpha)
                update_X_or_alpha = firsts[alpha].hard_update(local_first) or firsts[X].hard_update(local_first)
                change = change or update_X_or_alpha
    # First(Vt) + First(Vt) + First(RightSides)
    return firsts

def sentential_first(g_firsts:dict, SF:Symbol):
    
    """ - if X -> W1 | ... | Wn   :   First(X) = Union(First(Wi))
        - if X -> epsilon    :   epsilon is in First(X)
        - if W = xZ, x in Vt   :   First(W) = {x}
        - if W = YZ, Y in Vn, Z in SententialForm   :   First(Y) is in First(W)
        - if W = YZ and epsilon in First(Y)   :   First(Z) is in First(W)
    """
    first_SF = ContainerSet()
    if type(SF) is Terminal:
        first_SF.add(SF)
    elif SF.IsEpsilon:
        first_SF.set_epsilon()
    elif type(SF) is NonTerminal:
        for pr in SF.productions:
            # pr: X -> alpha
            alpha:Sentential_Form = pr.Body
            if alpha.IsEpsilon:
                # X -> epsilon    :   epsilon is in First(X)
                first_SF.set_epsilon()              
            else:
                # First(X) = Union(First(Wi))
                f_sf = sentential_first(g_firsts, alpha)
                first_SF.extend([v for v in f_sf])
                g_firsts[alpha] = f_sf                
    elif type(SF) is Sentential_Form:
        for sym in SF:
            # SF = xZ or SF = YZ

            #  W = xZ, x in Vt : First(W) = {x}
            if SF[0] == sym and type(sym) is Terminal: 
                first_SF.add(sym)
                break
            #  W = YZ : First(Y) is in First(W)
            f_sym = sentential_first(g_firsts, sym)            
            first_SF.extend([v for v in f_sym])

            # if epsilon in First(Y) : First(Z) is in First(W)
            if not f_sym.contains_epsilon:
                break          
            
    return first_SF

def Follow(grammar:Grammar, firsts:dict):
    """ A non-terminal Follow's set is defined by:
        $ is in Follow(S)
        epsilon is never in Follow(X)
        if X -> WAZ | W and Z sentential forms, A a non-teminal   :   First(Z) - {e} is in Follow(A)
        if X -> WAZ and epsilon in First(Z)   :   Follow(X) is in Follow(A)
    """
    follows = {}
    #init Follow(Vn)
    for nt in grammar.nonTerminals:
        follows[nt] = ContainerSet()
    follows[grammar.mainSymbol] = ContainerSet(G.EOF)
    change = True
    while change:
        change = False
        for pr in grammar.Productions:
            NT = pr.Head
            local_follow = ContainerSet()
            for PR in grammar.Productions:
                # X -> SF
                X = PR.Head
                SF = PR.Body
                nt_ind = -1
                if not SF.IsEpsilon:
                    for i in range(len(SF)):
                        if SF[i] == NT:
                            nt_ind = i
                            break
                    if nt_ind < 0: 
                        continue
                    #NT in SF
                    if nt_ind < len(SF) - 1: #not the last item in the SF
                        nt_next = SF[nt_ind + 1]
                        next_first = firsts[nt_next]
                        # firsts(nt_next) is in follow(NT)
                        local_follow.extend(x for x in next_first)
                        # if epsilon in first(nt_next), follow(X) also in follow(NT)
                        if next_first.contains_epsilon:
                            local_follow.update(follows[X])
                    else:
                            local_follow.update(follows[X])
                change = change or follows[NT].hard_update(local_follow)

    return follows

def LL_1_top_to_down_parser(grammar:Grammar, P_table:dict = None, firsts = None, follows = None):
    if P_table is None:
        if firsts is None: firsts = First(grammar)
        if follows is None: follows = Follow(grammar, firsts)
        P_table = LL_1_parsing_table(grammar, firsts, follows)
    
    def parser(w):
        if w[len(w) - 1] != grammar.EOF:
            w += grammar.EOF
        
        stack = [grammar.EOF, grammar.mainSymbol]
        cursor = 0
        output = []

        #parssing w
        while True:
            if len(stack) <= 0:
                break

            top:Symbol = stack.pop()
            # print(top)
            term:Token = w[cursor]
            if top.token_type == term.token_type:
                cursor+=1
            else:
                prod = P_table[(top,term)]
                prod:Production
                output.append(prod)
                if not prod.Body.IsEpsilon:
                    alpha = prod.Body

                    for i in range(len(alpha)-1,-1,-1):
                        stack.append(alpha[i])

        return output            

    return parser

def LL_1_recursive_descending_parser():

    pass

def LL_1_parsing_table(grammar:Grammar, firsts, follows):
    """LL(1) table:
        if X -> W and t in First(W)   :   T[X,t] = (X -> W)
        if X -> W and epsilon in First(W), and t in Follow(X)   :   T[X,t] = (X -> W)
        if there are two productions in T[X,t] th grammar isn't LL(1)
    """
    P_table = {}
    for pr in grammar.Productions:
        # X -> alpha
        pr:Production
        X = pr.Head
        alpha = pr.Body
        alpha_first = firsts[alpha]
        if alpha_first.contains_epsilon:
            X_follow = follows[X]
            for t in X_follow:
                cell = P_table.get((X,t))
                if cell:
                    if cell is Production and cell.Body.IsEpsilon:
                        P_table[(X,t)] = pr 
                    elif pr.Body.IsEpsilon:
                        pass
                    else: 
                        if cell is Production:
                            P_table[(X,t)] = [cell, pr]
                        else: P_table[(X,t)] = cell + [pr]
                        print('except: ',X, t, cell,' new:',pr)
                else: P_table[(X,t)] = pr 
        else:
            for t in alpha_first:
                cell = P_table.get((X,t))
                if cell:
                    print('except:',X,t,cell,' new:',pr)
                else: P_table[(X,t)] = pr 
    return P_table

def LR_1():
    pass

def SLR_1():
    pass

def LALR_1():
    pass

# G = Grammar()
# E = G.New_NonTerminal('E', fix_t['expression'], main_symbol=True)
# T = G.New_NonTerminal('T', fix_t['term'])
# F = G.New_NonTerminal('F', fix_t['factor'])
# X = G.New_NonTerminal('X', fix_t['FX'])
# Y = G.New_NonTerminal('Y', fix_t['UX'])
# plus = G.New_Terminal('+', fix_t['+'])
# minus = G.New_Terminal('-', fix_t['-'])
# star = G.New_Terminal('*', fix_t['*'])
# div = G.New_Terminal('/', fix_t['/'])
# opar = G.New_Terminal('(', fix_t['('])
# cpar = G.New_Terminal(')', fix_t[')'])
# num = G.New_Terminal('num', fix_t['decimal'])

# G.Add_Production(Production(E,Sentential_Form(T,X)))
# G.Add_Production(Production(X,Sentential_Form(plus,T,X)))
# G.Add_Production(Production(X,Sentential_Form(minus,T,X)))
# G.Add_Production(Production(X,G.Epsilon))
# G.Add_Production(Production(T,Sentential_Form(F,Y)))
# G.Add_Production(Production(Y,Sentential_Form(star,F,Y)))
# G.Add_Production(Production(Y,Sentential_Form(div,F,Y)))
# G.Add_Production(Production(Y,G.Epsilon))
# G.Add_Production(Production(F,Sentential_Form(num)))
# G.Add_Production(Production(F,Sentential_Form(opar,E,cpar)))
G = F0F_LL_1()
# print(G)

# E %= T + X
# X %= plus + T + X | minus + T + X | G.Epsilon
# T %= F + Y
# Y %= star + F + Y | div + F + Y | G.Epsilon
# F %= num | opar + E + cpar
 
firsts = First(G)
# print(firsts)
follows = Follow(G, firsts)
# print(follows)
ll_1_table  = LL_1_parsing_table(G, firsts, follows)
# print(ll_1_table)
# ll1_parser = LL_1_top_to_down_parser(G, ll_1_table, firsts, follows)
# print(ll1_parser([num, star, num, star, num, plus, num, star, num, plus, num, plus, num, G.EOF])) # "n * n * n + n * n + n + n $"
