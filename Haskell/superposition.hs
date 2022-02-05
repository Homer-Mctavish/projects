import Quipper

spos :: Bool -> Circ Qubit
spos b = do q <- qinit b
            r <- hadamard q
            return r
