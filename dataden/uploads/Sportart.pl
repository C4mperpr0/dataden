sportart(laufen).
sportart(schwimmen).

kann_gut(anne,laufen).
kann_gut(anne,schwimmen)

betreibt(anne,X):-
  sportart(X),
  kann_gut(anne,X).
betreibt(bernd,Y):-
  betreibt(anne,Y).
