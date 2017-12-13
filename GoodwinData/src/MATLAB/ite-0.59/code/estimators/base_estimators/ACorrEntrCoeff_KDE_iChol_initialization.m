function [co] = ACorrEntrCoeff_KDE_iChol_initialization(mult,post_init)
%function [co] = ACorrEntrCoeff_KDE_iChol_initialization(mult)
%function [co] = ACorrEntrCoeff_KDE_iChol_initialization(mult,post_init)
%Initialization of the Gaussian KDE (kernel density estimation) + incomplete Cholesky decomposition based correntropy coefficient estimator.
%
%Note:
%   1)The estimator is treated as a cost object (co).
%   2)We use the naming convention 'A<name>_initialization' to ease embedding new association measure estimator methods.
%
%INPUT:
%   mult: is a multiplicative constant relevant (needed) in the estimation; '=1' means yes (='exact' estimation), '=0' no (=estimation up to 'proportionality').
%   post_init: {field_name1,field_value1,field_name2,field_value2,...}; cell array containing the names and the values of the cost object fields that are to be used
%   (instead of their default values). For further details, see 'post_initialization.m'.
%OUTPUT:
%   co: cost object (structure).

%Copyright (C) 2012-2014 Zoltan Szabo ("http://www.gatsby.ucl.ac.uk/~szabo/", "zoltan (dot) szabo (at) gatsby (dot) ucl (dot) ac (dot) uk")
%
%This file is part of the ITE (Information Theoretical Estimators) toolbox.
%
%ITE is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by
%the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
%
%This software is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
%MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
%
%You should have received a copy of the GNU General Public License along with ITE. If not, see <http://www.gnu.org/licenses/>.

%mandatory fields (following the template structure of the estimators to make uniform usage of the estimators possible):
    co.name = 'CorrEntrCoeff_KDE_iChol';
    co.mult = mult;
    
%other fields:    
    co.sigma = 1;%std in the RBF (Gaussian) kernel
    
%post initialization (put it _before_ initialization of the members in case of a meta estimator):    
    if nargin==2 %there are given (name,value) cost object fields
        co = post_initialization(co,post_init);
    end    
   
