function [K] = analytical_value_KEJR2(distr1,distr2,u_K,par1,par2)
%function [K] = analytical_value_KEJR2(distr1,distr2,u_K,par1,par2)
%Analytical value (K) of the Jensen-Renyi kernel-2 for the given distributions. See also 'quick_test_KEJR2.m'.
%
%INPUT:
%   distr1 : name of the distribution-1.
%   distr2 : name of the distribution-2.
%   u_K    : parameter of the Jensen-Renyi kernel-2 (alpha_K = 2: fixed).
%   par1   : parameters of the distribution (structure).
%   par2   : parameters of the distribution (structure).
%
%If (distr1,distr2) = ('normal','normal'): par1.mean, par1.std <- N(m1,s1^2xI); par2.mean, par2.std <- N(m2,s2^2xI).

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

if strcmp(distr1,'normal') && strcmp(distr2,'normal') %Fei Wang, Tanveer Syeda-Mahmood, Baba C. Vemuri, David Beymer, and Anand Rangarajan. Closed-Form Jensen-Renyi Divergence for Mixture of Gaussians and Applications to Group-Wise Shape Registration. Medical Image Computing and Computer-Assisted Intervention, 12: 648–655, 2009. 
    m1 = par1.mean; s1 = par1.std;
    m2 = par2.mean; s2 = par2.std;
    
    w = [1/2;1/2];%parameter of Jensen-Renyi divergence, fixed
    ms = [m1,m2];
    ss = [s1,s2];
    term1 = compute_H2(w,ms,ss);
	term2 = w(1) * compute_H2(1,m1,s1) + w(2) * compute_H2(1,m2,s2);
	D  = term1 - term2; %H2(\sum_i wi Yi) - \sum_i w_i H2(Yi), where H2 is the quadratic Renyi entropy
    
    K = exp(-u_K*D);
else
    error('Distribution=?');                 
end
            
