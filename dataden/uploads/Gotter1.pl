% Autor: 
% Datum:  
 
maennlich(uranos).
maennlich(kronos).
maennlich(hades).
maennlich(poseidon).
maennlich(zeus). 
maennlich(ares). 
maennlich(apollon). 
maennlich(hephaistos).

weiblich(gaia).
weiblich(rhea).
weiblich(hestia).
weiblich(demeter).
weiblich(hera). 
weiblich(leto). 
weiblich(metis). 
weiblich(athene). 
weiblich(artemis).

elternteil(uranos,kronos). elternteil(gaia, kronos). %kronos
elternteil(uranos,rhea). elternteil(gaia, rhea). %rhea
elternteil(kronos,hades). elternteil(rhea, hades). %hades
elternteil(kronos,poseidon). elternteil(rhea, poseidon). %poseidon
elternteil(kronos,zeus). elternteil(rhea, zeus). %zeus
elternteil(kronos,hestia). elternteil(rhea, hestia). %hestia
elternteil(kronos,demeter). elternteil(rhea, demeter). %demeter
elternteil(kronos,hera). elternteil(rhea, hera). %hera

elternteil(zeus, ares). elternteil(hera, ares). %ares
elternteil(zeus, hephaistos). elternteil(hera, hephaistos). %hephaistos
elternteil(zeus, apollon). elternteil(leto, apollon). %apollon
elternteil(zeus, artemis). elternteil(leto, artemis). %artemis
elternteil(zeus, athene). elternteil(metis, athene). %athene

vorfahr(X,Y):-elternteil(X,Y).
vorfahr(X,Y) :- elternteil(X,Z), vorfahr(Z,Y).

kind(X,Y):- elternteil(Y,X).
nachkomme(X,Y):- kind(X,Y).
nachkomme(X,Y):- (kind(X,Z),nachkomme(Z,Y)).