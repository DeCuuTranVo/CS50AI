from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    ## Information about the structure of the problem 
    # AKnight and AKnave can not be true at the same time: AKnight XOR AKnave
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    
    ## That the characters actually said
    # A says "I am both a knight and a knave."
    Implication(AKnight, And(AKnight, AKnave)), # if A is a Knight, then A tells the truth
    Implication(AKnave, Not(And(AKnight, AKnave))) # if A is a Knave, then A tells the falsity
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    ## Information about the structure of the problem 
    # AKnight and AKnave can not be true at the same time: AKnight XOR AKnave, 
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    # BKnight and BKnave can not be true at the same time: BKnight XOR BKnave,
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    
    ## That the characters actually said
    # A says "We are both knaves."
    Implication(AKnight, And(AKnave, BKnave)), # if A is a Knight, then A tells the truth
    Implication(AKnave, Not(And(AKnave, BKnave))), # if A is a Knave, then A tells the falsity
    # B says nothing
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    ## Information about the structure of the problem 
    # AKnight and AKnave can not be true at the same time: AKnight XOR AKnave, 
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    # BKnight and BKnave can not be true at the same time: BKnight XOR BKnave,
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    
    ## That the characters actually said
    # A says "We are the same kind."
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))), # if A is a Knight, then A tells the truth
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))), # if A is a Knave, then A tells the falsity
    # B says "We are of different kinds."
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))), # if B is a Knight, then B tells the truth
    Implication(BKnave, Or(And(AKnight, BKnight), And(AKnave, BKnave))) # if B is a Knave, then B tells the falsity
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    ## Information about the structure of the problem 
    # AKnight and AKnave can not be true at the same time: AKnight XOR AKnave, 
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    # BKnight and BKnave can not be true at the same time: BKnight XOR BKnave,
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    # CKnight and CKnave can not be true at the same time: CKnight XOR CKnave,
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),
    
    ## That the characters actually said
    # A says either “I am a knight.” or “I am a knave.”, but you don’t know which.
    Or( # I don't know which statements is true
        And( # A says “I am a knight.”
            Implication(AKnight, AKnight), # if A is a Knight, then A tells the truth
            Implication(AKnave, Not(AKnight)), # if A is a Knave, then A tells the lie
        ),
        And( # A says “I am a knave.”
            Implication(AKnight, AKnave), # if A is a Knight, then A tells the truth
            Implication(AKnave, Not(AKnave)), # if A is a Knave, then A tells the lie
        ),
    ),

    # B says "A said 'I am a knave'."
    Implication(BKnight,  # if B is a Knight, then B tells the truth;
                And(
                    Implication(AKnight, AKnave), # if A is a Knight, then A tells the truth
                    Implication(AKnave, Not(AKnave)) # if A is a Knave, then A tells the lie
                    )
    ), 
    
    Implication(BKnave, # if B is a Knave, then B tells the lie;
                Not(
                    And(
                        Implication(AKnight, AKnave), # if A is a Knight, then A tells the truth
                        Implication(AKnave, Not(AKnave)) # if A is a Knave, then A tells the lie
                    )
                )
    ),
    
    # B says "C is a knave."
    Implication(BKnight, CKnave), # if B is a Knight, then B tells the truth
    Implication(BKnave, Not(CKnave)), # if B is a Knave, then B tells the falsity
    
    # C says "A is a knight."
    Implication(CKnight, AKnight), # if C is a Knight, then C tells the truth
    Implication(CKnave, Not(AKnight)) # if C is a Knave, then C tells the falsity
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
